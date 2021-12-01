import csv
from itertools import chain, combinations

def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))

def parser(path):
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        meta = {}
        projects = {}
        votes = []
        section = ""
        header = []
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ["meta", "projects", "votes"]:
                section = str(row[0]).strip().lower()
                header = next(reader)
            elif section == "meta":
                meta[row[0]] = row[1].strip()
            elif section == "projects":
                projects[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it+1].strip()
            elif section == "votes":
                votes.append({})
                for it, key in enumerate(header[1:]):
                    votes[-1][key.strip()] = row[it+1].strip()
                votes[-1]['vote'] = votes[-1]['vote'].split(',')
                votes[-1]['vote'] = set([v for v in votes[-1]['vote']])
        items = projects.keys()
        max_cost = float(meta['budget'])
        costs = {}
        for item in items:
            costs[item] = float(projects[item]['cost'])
        return votes, items, costs, max_cost

def num_satisfaction(budget, voter, costs):
    return len(budget.intersection(voter['vote']))

def cost_satisfaction(budget, voter, costs):
    covered = budget.intersection(voter['vote'])
    return total_cost(covered, costs)

def binary_satisfaction(budget, voter, costs):
    return num_satisfaction(budget, voter, costs) > 0

def total_cost(budget, costs):
    cost = 0
    for it in budget:
        cost += costs[it]
    return cost

def max_rule(items, voters, costs, max_cost, satisfaction_fn):
    subsets = all_subsets(items)
    best_set = set([])
    max_score = 0
    for budget in subsets:
        if (total_cost(budget, costs) > max_cost):
            continue
        score = sum([satisfaction_fn(set(budget), v, costs) for v in voters])
        if score > max_score:
            max_score = score
            best_set = budget
    return best_set

def greedy_rule(items, voters, costs, max_cost, satisfaction_fn):
    cur_budget = set([])
    cur_cost = 0
    items_set = set(items)
    while (cur_cost < max_cost):
        best_item = None
        best_score = 0
        for it in items:
            if(costs[it] + cur_cost > max_cost or it in cur_budget):
                continue
            score = sum([satisfaction_fn(cur_budget | set([it]), v, costs) for v in voters])
            if (score >= best_score):
                best_score = score
                best_item = it
        if not best_item:
            break
        cur_budget.add(best_item)
        cur_cost += costs[best_item]
    return cur_budget

def prop_greedy_rule(items, voters, costs, max_cost, satisfaction_fn):
    cur_budget = set([])
    cur_cost = 0
    cur_score = 0
    items_set = set(items)
    while (cur_cost < max_cost):
        best_item = None
        best_score = 0
        best_norm_score = 0
        for it in items:
            if(costs[it] + cur_cost > max_cost or it in cur_budget):
                continue
            score = sum([satisfaction_fn(cur_budget | set([it]), v, costs) for v in voters])
            norm_score = (score - cur_score) / costs[it]
            if (norm_score >= best_norm_score):
                best_score = score
                best_norm_score = norm_score
                best_item = it
        if not best_item:
            break
        cur_budget.add(best_item)
        cur_score = best_score
        cur_cost += costs[best_item]
    return cur_budget

def anger_ratio(voters, budget):
    total_anger = sum([binary_satisfaction(budget, v, None) == 0 for v in voters])
    return total_anger / len(voters)

def ave_cost(budget, costs):
    total_cost = sum([costs[it] for it in budget])
    return total_cost / len(budget)

if __name__ == "__main__":
    votes, items, costs, max_cost = parser('poland_warszawa_2019_siekierki-augustowka.pb')
    print(total_cost(items, costs))
    print("GREEDY NUM_SAT")
    budget = greedy_rule(items, votes, costs, max_cost, num_satisfaction)
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("GREEDY COST_SAT")
    budget = greedy_rule(items, votes, costs, max_cost, cost_satisfaction)
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("GREEDY BIN_SAT")
    budget = greedy_rule(items, votes, costs, max_cost, binary_satisfaction)
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("PROP GREEDY NUM_SAT")
    print(prop_greedy_rule(items, votes, costs, max_cost, num_satisfaction))
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("PROP GREEDY COST_SAT")
    print(prop_greedy_rule(items, votes, costs, max_cost, cost_satisfaction))
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("PROP GREEDY BIN_SAT")
    print(prop_greedy_rule(items, votes, costs, max_cost, binary_satisfaction))
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("MAX NUM_SAT")
    print(max_rule(items, votes, costs, max_cost, num_satisfaction))
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("MAX COST_SAT")
    print(max_rule(items, votes, costs, max_cost, cost_satisfaction))
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

    print("----")
    print("MAX BIN_SAT")
    print(max_rule(items, votes, costs, max_cost, binary_satisfaction))
    print("ANGER: ", anger_ratio(votes, budget))
    print("AVE COST: ", ave_cost(budget, costs))

