# -*- coding: utf-8 -*-

import numpy as np
from constants import DEFAULT, FIXHEAT, FIXTEMP, RHO
from surface import connection_matrix

def wind_pressure(rho, vel, pressure_coefficient):
    ''' calculate wind pressure'''
    return 0.5*rho*vel*vel*pressure_coefficient

def buoy_pressure(height, ext_temp, int_temp):
    ''' calculate buoyancy pressure'''
    return -3455*height*((1/(ext_temp+273.15))-(1/(int_temp+273.15)))

def resid_calc(room_press, step, balance, count, flow_rate):
    '''adjust room pressures and step'''
    for i, _rp in enumerate(room_press):
        if balance[i] < 0:
            room_press[i] = room_press[i]-step[i]
            step[i] = 0.98*step[i]
            if count%1000 == 0:
                room_press[i] = 0 # Reset the pressure if using
                step[i] = 10000/count
                step[i] = abs(balance[i]*room_press[i]/(np.amax(flow_rate[i]) + 0.00001))
                # max(balance/(np.amax(flow_rate_matrix, 1)+0.000001))
        else:
            pass
    return room_press, step

def mech_pressures(bool_mech, driving_press, room_press, connections):
    '''driving pressures for mechanical inlet/outlet'''
    for i, bool_m in enumerate(bool_mech):
        if bool_m:
            for j in range(len(connections.T)):
                for k in range(len(connections.T[j])):
                    if j == i and connections[k, j]:
                        driving_press[i] = room_press[k]
    return driving_press

def internal_driving(bool_int, num_zones, ext_press, room_press, connections):
    ''' set internal driving pressures to adjacent room'''
    if num_zones == 1: #can't have internal openings if only one zone
        return ext_press

    for i, bool_i in enumerate(bool_int):
        if bool_i:
            for j in range(0, num_zones):
                for k in range(0, num_zones):
                    if j != k and connections[j, i] == connections[k, i]:
                        ext_press[j, i] = room_press[k]
                        #TODO add hydostatic pressure differences.
    return ext_press


def flows(flow_coeff, press_drop, exponent, connections):
    '''governing flow equation'''
    divisor = abs(press_drop)
    numerator = press_drop
    numerator[divisor == 0] = 1
    divisor[divisor == 0] = 1
    #result = np.nan_to_num(flow_coeff*(abs(press_drop)**exponent)*(numerator/divisor)*connections)
    result = flow_coeff*(abs(press_drop)**exponent)*(numerator/divisor)*connections

    return result

def driving_press(building):
    result = wind_pressure(RHO, building.weather.wind_speed, building.wind_coeff) + \
                    buoy_pressure(building.height, building.weather.ext_temp, building.room_temps)
    result = mech_pressures(building.bool_mech, result,
                                       building.room_press, building.connections)
    return result

def recalcroomtemps(room_temps, flow_rate_matrix, connections, internal_gains, building):
    #let's loop through the rooms.
    new_room_temps = []
    for i, r in enumerate(room_temps):
        flows = flow_rate_matrix[i]

        #get the adjacent temperatures.
        adj_temp = []
        for j, f in enumerate(flows):
            if building.bool_internal[j] == True:
                append_this = building.weather.ext_temp
                for k, row in enumerate(connections):
                    if k != i and row[j]>0 :
                        append_this = room_temps[k]
                adj_temp.append(append_this)
            elif building.bool_internal[j] == False:
                adj_temp.append(building.weather.ext_temp)
        
        adj_temp = np.array(adj_temp)
        #adj_temp = np.array(building.num_openings*[building.weather.ext_temp])
        net_flow = np.sum(flows[flows>0])
        if net_flow==0:
            new_room_temps.append(r)
        else:
            gain_component = building.internal_gains[i]/(1005*1.2)
            flow_component = np.sum(adj_temp[flows>0]*flows[flows>0])
            new_r = 0.7*r + 0.3* min(40,(gain_component + flow_component)/(net_flow))
            new_room_temps.append(new_r)
    return np.array(new_room_temps)

def solve_airflow(building, weather, analysis_settings, print_message=True, temp_type=DEFAULT):
    ''' solve the pressure flows'''
    building.weather = weather
    
    ##Load some things for speed###
    bool_internal = building.bool_internal
    flow_coeff = building.flow_coeff
    exponent = building.exponent
    room_press = building.room_press
    room_temps = building.room_temps
    height = building.height
    bool_mech = building.bool_mech
    
    if temp_type==DEFAULT:
        room_temps = np.array(building.num_openings*[weather.int_temp])
    elif temp_type==FIXTEMP:
        room_temps = np.array(building.num_openings*[weather.int_temp])
    elif temp_type==FIXHEAT:
        #First pass use external temperature.
        room_temps = np.array(building.num_openings*[weather.ext_temp + 2]) #Make it slightly warmer
    
    building.room_temps = room_temps
    building.connections = connection_matrix(building)
    #print(building.connections)

    ### Initial Values###
    try:
        room_press = np.min(driving_press(building)[np.nonzero(driving_press(building))], axis=0)
    except:
        room_press = np.array(building.num_zones*[-100])
    step = np.array(building.num_zones*[np.mean(room_press)]) #Iteration pressure step
    step = np.abs(step)

    count = 0 #Iteration counter
    balance = np.array(building.num_zones*[-1]) #Flow balance

    flow_rate_matrix = np.ones([building.num_zones, building.num_openings]) #Calculated flow rate

    track = []
    steptrack = []
    steptrack.append(step.tolist())
    perc_error = analysis_settings.airflow['percerror']
    
    driving_pressure_store = driving_press(building)
    
    while((min(balance/(np.amax(flow_rate_matrix, 1)+0.000001)) < -perc_error \
           or max(balance/(np.amax(flow_rate_matrix, 1)+0.000001)) > perc_error) \
           and count < 9999):

        room_press = room_press+0.5*step #Iteration correction.
        count += 1
        if temp_type==FIXHEAT:
            #Recalutate room temperatures.
            pass#room_temps = self.calcroomtemps()
        #driving_press = mech_pressures(self.bool_mech(), driving_press,
        #                               room_press, self.connections)
        
        if True:
            driving_pressure_store = driving_press(building)
        
        ext_press = driving_pressure_store*building.connections #driving pressure

        #The driving pressure on a connected opening is the adjacent room.
        ext_press = internal_driving(bool_internal, building.num_zones, ext_press,
                                     room_press, building.connections)
        ext_press = ext_press*building.connections
        #Pressure drop across openings.
        press_drop = np.transpose(np.transpose(ext_press) - room_press) \
                     + np.transpose((1-building.connections).T*room_press)

        #Pressure difference across each flow path.
        flow_rate_matrix = flows(flow_coeff, press_drop, exponent, building.connections)
        balance = sum(np.transpose(flow_rate_matrix))

        if building.num_zones == 1:
            #some exceptions for if there is only one zone.
            balance = np.array(building.num_zones*[balance])
            flow_rate_matrix = np.array([flow_rate_matrix])


        if temp_type==FIXHEAT:
            #Recalutate room temperatures.
            room_temps = recalcroomtemps(room_temps, flow_rate_matrix, building.connections, room_temps, building)

        #print(room_temps)
        #print(flow_rate_matrix[0])
        room_press, step = resid_calc(room_press, step, balance, count, flow_rate_matrix)
        track.append(room_press)
        steptrack.append(step.tolist())

    building.flow_rate = np.array([max(x) for x in flow_rate_matrix.T])
    #self.flow_rate = flow_rate
    #print(room_temps)
    building.room_temps = room_temps
    
    building.room_press = room_press
    if print_message:
        print("Flow rate\n", building.flow_rate, "m3/s\n")
        print("Imbalance\n", balance, "m3/s")
        print(np.array([np.sum(balance)]), "m3/s Total")
        print(100*balance/(np.amax(flow_rate_matrix, 1)), "%")
        print(100*np.array([np.sum(balance)])/(np.sum(np.amax(flow_rate_matrix, 1))), "% Total\n")
        print("Room Pressures\n", room_press, "Pa\n")
        print("ext press\n", ext_press, "Pa\n")
        #print("Pressure Drop\n", press_drop, "Pa\n")
        #print("Increment\n", step, "\n")
        print("Steps\n", count, "\n")
        print("Flow paths\n", flow_rate_matrix, "m3/s\n")
        print("Room Temps\n", building.room_temps, "degC")

    return track, steptrack