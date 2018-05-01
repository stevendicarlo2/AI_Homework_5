TEAM_NAME = "yungAIthugz" #Pick a team name
MEMBERS = ["snd7nb", "yq4du"] #Include a list of your members’ UVA IDs


def get_move(state):
    game = state["game"]
    team_code = state["team-code"]

    info = load_data()
    if info == {}:
        info = initialize_info()

    if game == "phase_1":
        info = handle_phase_1_info(state, info)

        try:
            move = get_phase_1_move(state, info)
        except:
            move = None

        info["last_pull"] = move
        save_data(info)

        return {
            "team-code": team_code,
            "game": game,
            "pull": move
        }
    elif game == "phase_2_a":
        try:
            move = get_phase_2a_move(info)
        except:
            move = []
        return {
            "team-code": team_code,
            "game": game,
            "auctions": move
        }
    elif game == "phase_2_b":
        try:
            move = get_phase_2b_move()
        except:
            move = 1
        return {
            "team-code": team_code,
            "game": game,
            "bid": move
        }


def initialize_info():
    slot_history = [[] for _ in range(100)]
    remaining_credits = 1000000
    last_pull = None
    return {
        "slot_history": slot_history,
        "remaining_credits": remaining_credits,
        "last_pull": last_pull
    }

def get_phase_1_move(state, info):
    pulls_left = state["pulls-left"]
    remaining_credits = info["remaining_credits"]
    if pulls_left < 1 or remaining_credits < 100:
        return None

    slot_history = info["slot_history"]
    for slot_num in range(len(slot_history)):
        if len(slot_history[slot_num]) == 0:
            return slot_num
    return None


def handle_phase_1_info(state, info):
    last_pull = info["last_pull"]
    last_payoff = state["last-payoff"]
    last_cost = state["last-cost"]

    if last_pull is None or last_payoff is None or last_cost is None:
        return info

    net = last_payoff - last_cost
    info["slot_history"][last_pull].append(net)
    info["remaining_credits"] = info["remaining_credits"] - net
    return info


def get_phase_2a_move(info):
    slot_history = info["slot_history"]
    modified_slot_history = []
    for i in range(len(slot_history)):
        record = slot_history[i]
        if len(record) == 0:
            average_net = 0
        else:
            average_net = sum(record)/len(record)
        modified_slot_history.append((i, average_net))
    def sort_key(element):
        return element[1]
    sorted_slot_history = sorted(modified_slot_history, key=sort_key, reverse=True)
    best_slot_to_pick = 20
    worst_slot_to_pick = 30
    slots_to_pick = sorted_slot_history[best_slot_to_pick:worst_slot_to_pick]
    return_list = []
    for slot_info in slots_to_pick:
        return_list.append(slot_info[0])
    return return_list


def get_phase_2b_move():
    return 1


def load_data():
    return {
        "slot_history": [
            [],
            [4.3, 9.4],
            [4],
            [3],
            [1],
            [2]
        ],
        "remaining_credits": 103893,
        "last_pull": 0
    }


def save_data(info):
    return


sample_state = {
   "team-code": "eef8976e",
   "game": "phase_2_a",
}


print(get_move(sample_state))
