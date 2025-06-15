import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random


def normal_generator(mean, std):
    return np.random.normal(loc=mean, scale=std)

fel = []  # Future Event List

Nm = Nk = Nmw = Nkw = 0
SVRm = SVRk = 0
Sm = Sk = 0
Q1 = Q2 = 0
Qw = Qw2 = 0
TWT = 0
ML = MR = 0
Total_wt_for_return = Total_wt_for_borrow = 0

next_customer_id = 0

wait_lst = []     
checker_lst = []   
ABT_lst = []     
AMT_lst = []       

customers = {}    
morad_status = 'idle'
key_status = 'idle'

Tnow = 0
T1 = 10 * 60      
T2 = 11 * 60

random.seed(42)
sample_random = np.random.rand(10000)

def schedule_event(code, time, cust_id=None):
    fel.append((code, time, cust_id))


schedule_event(1, abs(normal_generator(30, 30)), None)
schedule_event(2, abs(normal_generator(30, 30)), None)
schedule_event(5, 0, None)  

def entering_system_for_borrowing(Tnow, cust_id):
    global fel, Nm, Nk, Sm, Sk, Q1, Q2, Qw, Qw2, TWT
    global ML, MR, next_customer_id, sample_random, checker_lst, ABT_lst
    global customers, morad_status, key_status

    ML += 1
    customers[cust_id] = {'state': 'waiting_Q1'}
    schedule_event(1, Tnow + abs(normal_generator(30, 30)), next_customer_id)

    if Sm == 0:
        Sm = 1
        morad_status = 'serving_Q1'
        Nm += 1
        customers[cust_id]['state'] = 'in_service_Q1'
        ST = abs(normal_generator(10, 5))
        ABT_lst.append(ST)
        schedule_event(3, Tnow + ST, cust_id)
    elif Sk == 0:
        Sk = 1
        key_status = 'serving_Q1'
        Nk += 1
        customers[cust_id]['state'] = 'in_service_Q1'
        ST = abs(normal_generator(14, 4))
        ABT_lst.append(ST)
        schedule_event(4, Tnow + ST, cust_id)
    else:
        Q1 += 1
        checker_lst.append(1)
        customers[cust_id]['state'] = 'waiting_Q1'
        wait_lst.append((cust_id, Tnow))

def entering_system_for_returning(Tnow, cust_id):
    global fel, Nm, Nk, Sm, Sk, Q1, Q2, Qw, Qw2, TWT
    global ML, MR, next_customer_id, sample_random, checker_lst
    global customers, morad_status, key_status

    MR += 1
    customers[cust_id] = {'state': 'waiting_Q1'}
    schedule_event(2, Tnow + abs(normal_generator(30, 30)), next_customer_id)

    if Sm == 0:
        Sm = 1
        morad_status = 'serving_Q1'
        Nm += 1
        customers[cust_id]['state'] = 'in_service_Q1'
        ST = 2
        schedule_event(3, Tnow + ST, cust_id)
    elif Sk == 0:
        Sk = 1
        key_status = 'serving_Q1'
        Nk += 1
        customers[cust_id]['state'] = 'in_service_Q1'
        ST = 2
        schedule_event(4, Tnow + ST, cust_id)
    else:
        Q1 += 1
        checker_lst.append(2)
        customers[cust_id]['state'] = 'waiting_Q1'
        wait_lst.append((cust_id, Tnow))

def service_end_morad(Tnow, cust_id):
    global fel, Nm, Nk, Sm, Sk, Q1, Q2, Qw, Qw2, TWT
    global Total_wt_for_borrow, Total_wt_for_return, checker_lst, customers, morad_status
    if cust_id is None:
        return
    Q2 += 1
    customers[cust_id]['state'] = 'waiting_Q2'

    if Q1 > 0:
        next_code = checker_lst.pop(0)
        Qw += 1
        Q1 -= 1
        (next_id, arr_time) = wait_lst.pop(0)
        WT = Tnow - arr_time
        TWT += WT
        if next_code == 1:
            Total_wt_for_borrow += WT
            ST = abs(normal_generator(10, 5))
        else:
            Total_wt_for_return += WT
            ST = 2
        customers[next_id]['state'] = 'in_service_Q1'
        Nm += 1
        morad_status = 'serving_Q1'
        schedule_event(3, Tnow + ST, next_id)
    else:
        Sm = 0
        morad_status = 'idle'

def service_end_keykavoos(Tnow, cust_id):
    global fel, Nm, Nk, Sm, Sk, Q1, Q2, Qw, Qw2, TWT
    global Total_wt_for_borrow, Total_wt_for_return, checker_lst, customers, key_status, Nkw
    if cust_id is None:
        return
    if customers[cust_id]['state'] == 'in_service_Q1':
        Q2 += 1
        customers[cust_id]['state'] = 'waiting_Q2'
    else:
        customers[cust_id]['state'] = 'done'
        Nkw += 1

    if Q1 > 0:
        next_code = checker_lst.pop(0)
        Qw += 1
        Q1 -= 1
        (next_id, arr_time) = wait_lst.pop(0)
        WT = Tnow - arr_time
        TWT += WT
        if next_code == 1:
            Total_wt_for_borrow += WT
            ST = abs(normal_generator(14, 4))
        else:
            Total_wt_for_return += WT
            ST = 2
        customers[next_id]['state'] = 'in_service_Q1'
        Nk += 1
        key_status = 'serving_Q1'
        schedule_event(4, Tnow + ST, next_id)
    elif Q2 > 0:
        Qw2 += 1
        Q2 -= 1
        customers[cust_id]['state'] = 'in_service_Q2'
        ST = abs(normal_generator(16, np.sqrt(52)))
        AMT_lst.append(ST)
        key_status = 'serving_Q2'
        schedule_event(5, Tnow + ST, cust_id)
    else:
        Sk = 0
        key_status = 'idle'

def service_end_warehouse(Tnow, cust_id):
    global Sk, Q1, Q2, Qw, Qw2, TWT, Total_wt_for_borrow, Total_wt_for_return, checker_lst, customers, key_status, Nk
    if cust_id is None:
        return
    customers[cust_id]['state'] = 'done'
    Nk += 1

    if Q2 > 0:
        Qw2 += 1
        Q2 -= 1
        customers[cust_id]['state'] = 'in_service_Q2'
        ST = abs(normal_generator(16, np.sqrt(52)))
        AMT_lst.append(ST)
        key_status = 'serving_Q2'
        schedule_event(5, Tnow + ST, cust_id)
    elif Q1 > 0:
        next_code = checker_lst.pop(0)
        Qw += 1
        Q1 -= 1
        (next_id, arr_time) = wait_lst.pop(0)
        WT = Tnow - arr_time
        TWT += WT
        if next_code == 1:
            Total_wt_for_borrow += WT
            ST = abs(normal_generator(14, 4))
        else:
            Total_wt_for_return += WT
            ST = 2
        customers[next_id]['state'] = 'in_service_Q1'
        Nk += 1
        key_status = 'serving_Q1'
        schedule_event(4, Tnow + ST, next_id)
    else:
        Sk = 0
        key_status = 'idle'

def service_warehouse_after_six_morad(Tnow, cust_id):
    global Nmw, Q2, AMT_lst, morad_status
    if cust_id is None:
        return
    Nmw += 1
    customers[cust_id]['state'] = 'in_service_Q2'
    ST = abs(normal_generator(16, np.sqrt(52)))
    AMT_lst.append(ST)
    morad_status = 'serving_Q2'
    schedule_event(6, Tnow + ST, cust_id)

def service_warehouse_after_six_keykavoos(Tnow, cust_id):
    global Nkw, Q2, AMT_lst, key_status
    if cust_id is None:
        return
    Nkw += 1
    customers[cust_id]['state'] = 'in_service_Q2'
    ST = abs(normal_generator(16, np.sqrt(52)))
    AMT_lst.append(ST)
    key_status = 'serving_Q2'
    schedule_event(7, Tnow + ST, cust_id)


history = []

while True:
    if not fel:
        break
    fel.sort(key=lambda x: x[1])
    event_code, event_time, cust_id = fel.pop(0)
    Tnow = event_time

    if Tnow > T1:
        break

    if event_code == 1:
        entering_system_for_borrowing(Tnow, next_customer_id)
        next_customer_id += 1
    elif event_code == 2:
        entering_system_for_returning(Tnow, next_customer_id)
        next_customer_id += 1
    elif event_code == 3:
        service_end_morad(Tnow, cust_id)
    elif event_code == 4:
        service_end_keykavoos(Tnow, cust_id)
    elif event_code == 5:
        service_end_warehouse(Tnow, cust_id)
    elif event_code == 6:
        service_warehouse_after_six_morad(Tnow, cust_id)
    elif event_code == 7:
        service_warehouse_after_six_keykavoos(Tnow, cust_id)

    history.append((Tnow, Q1, Q2, Sm, Sk, morad_status, key_status))


warehouse1_pos = (2, 8)
warehouse2_pos = (8, 8)
Q1_x = 2
Q2_x = 8
Q1_y_top = 6
Q2_y_top = 4

frames = []
for (time_stamp, q1, q2, sm, sk, m_status, k_status) in history:
    cust_positions = []
    for i in range(q1):
        cust_positions.append((Q1_x, Q1_y_top - i * 0.5))
    for i in range(q2):
        cust_positions.append((Q2_x, Q2_y_top - i * 0.5))

    if m_status == 'idle':
        morad_px, morad_py = warehouse1_pos[0], warehouse1_pos[1] - 1
        morad_color = 'green'
    elif m_status == 'serving_Q1':
        morad_px, morad_py = warehouse1_pos
        morad_color = 'red'
    else:
        morad_px, morad_py = warehouse2_pos
        morad_color = 'red'

    if k_status == 'idle':
        key_px, key_py = warehouse2_pos[0], warehouse2_pos[1] - 1
        key_color = 'green'
    elif k_status == 'serving_Q1':
        key_px, key_py = warehouse1_pos
        key_color = 'red'
    else:
        key_px, key_py = warehouse2_pos
        key_color = 'red'

    frames.append({
        'time': time_stamp,
        'cust_positions': np.array(cust_positions) if cust_positions else np.empty((0, 2)),
        'morad_pos': (morad_px, morad_py),
        'morad_color': morad_color,
        'key_pos': (key_px, key_py),
        'key_color': key_color
    })


fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

ax.add_patch(plt.Rectangle((warehouse1_pos[0] - 0.5, warehouse1_pos[1] - 0.5), 1, 1, color='lightgray'))
ax.add_patch(plt.Rectangle((warehouse2_pos[0] - 0.5, warehouse2_pos[1] - 0.5), 1, 1, color='lightgray'))
ax.text(warehouse1_pos[0], warehouse1_pos[1] + 0.7, 'Warehouse 1', ha='center')
ax.text(warehouse2_pos[0], warehouse2_pos[1] + 0.7, 'Warehouse 2', ha='center')
ax.text(warehouse1_pos[0] - 1, warehouse1_pos[1] - 5, 'Q1', ha='center')
ax.text(warehouse2_pos[0] + 1, warehouse2_pos[1] - 5, 'Q2', ha='center')


cust_scat = ax.scatter([], [], s=100, c='green', marker='o', label='Customers')
morad_dot = ax.scatter([], [], s=200, c='green', marker='s', label='Morad')
key_dot   = ax.scatter([], [], s=200, c='green', marker='s', label='Keykavoos')

time_text = ax.text(0.5, 9.5, '', ha='center')

def init_anim():
    cust_scat.set_offsets(np.empty((0, 2)))
    morad_dot.set_offsets(np.empty((0, 2)))
    key_dot.set_offsets(np.empty((0, 2)))
    return cust_scat, morad_dot, key_dot, time_text

def update_anim(i):
    frame = frames[i]
    cust_scat.set_offsets(frame['cust_positions'])
    morad_dot.set_offsets([frame['morad_pos']])
    morad_dot.set_color(frame['morad_color'])
    key_dot.set_offsets([frame['key_pos']])
    key_dot.set_color(frame['key_color'])
    time_text.set_text(f"Time = {int(frame['time'])} min")
    return cust_scat, morad_dot, key_dot, time_text

ani = animation.FuncAnimation(fig, update_anim, frames=len(frames),
                            init_func=init_anim, blit=True, interval=250, repeat=False)

plt.legend(loc='lower left')
plt.show()
