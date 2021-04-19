# Jeb Barker 4/19/21
from pomegranate import *

def main():
    Graduation = DiscreteDistribution({'graduated': .9, 'failed': 0.1})
    Offer1 = ConditionalProbabilityTable([
        ['graduated', 'offered', .5],
        ['graduated', 'rejected', .5],
        ['failed', 'offered', .05],
        ['failed', 'rejected', .95]], [Graduation])
    Offer2 = ConditionalProbabilityTable([
        ['graduated', 'offered', .75],
        ['graduated', 'rejected', .25],
        ['failed', 'offered', .25],
        ['failed', 'rejected', .75]], [Graduation])
    s_grad = State(Graduation, 'graduation')
    s_offer_1 = State(Offer1, 'offer_1')
    s_offer_2 = State(Offer2, 'offer_2')
    model = BayesianNetwork('student')
    model.add_states(s_grad, s_offer_1, s_offer_2)
    model.add_transition(s_grad, s_offer_1)
    model.add_transition(s_grad, s_offer_2)
    model.bake()  # finalize the topology of the model
    print('The number of nodes:', model.node_count())
    print('The number of edges:', model.edge_count())
    print("Pop-Quiz Check: \na)")
    # predict_proba(Given factors)
    # P(~o2 | g, ~o1) and P(o2 | g, ~o1)
    print(model.predict_proba({'graduation': 'graduated', 'offer_1': 'rejected'})[2].parameters)
    # P(g | o1, o2) and P(~g | o1, o2)
    print("b)\n", model.predict_proba({'offer_1': 'offered', 'offer_2': 'offered'})[0].parameters)
    # P(g | ~o1, o2) and P(~g | ~o1, o2)
    print("c)\n", model.predict_proba({'offer_1': 'rejected', 'offer_2': 'offered'})[0].parameters)
    # P(g | ~o1, ~o2) and P(~g | ~o1, ~o2)
    print("d)\n", model.predict_proba({'offer_1': 'rejected', 'offer_2': 'rejected'})[0].parameters)
    # P(o2 | o1) and P(~o2 | o1)
    print("e)\n", model.predict_proba({'offer_1': 'offered'})[2].parameters)

    Sun = DiscreteDistribution({'sunny': .7, 'not-sunny': 0.3})
    Salary = DiscreteDistribution({'salary-raise': .01, 'no-raise': 0.99})
    Happiness = ConditionalProbabilityTable([
        ['sunny', 'salary-raise', 'happy', 1.0],
        ['sunny', 'salary-raise', 'sad', 0.0],
        ['not-sunny', 'salary-raise', 'happy', .9],
        ['not-sunny', 'salary-raise', 'sad', .1],
        ['sunny', 'no-raise', 'happy', .7],
        ['sunny', 'no-raise', 'sad', .3],
        ['not-sunny', 'no-raise', 'happy', .1],
        ['not-sunny', 'no-raise', 'sad', .9]],
        [Sun, Salary])
    s_sun = State(Sun, 'sun')
    s_offer = State(Salary, 'offer')
    s_happiness = State(Happiness, 'happiness')
    model = BayesianNetwork('mood')
    model.add_states(s_sun, s_offer, s_happiness)
    model.add_transition(s_sun, s_happiness)
    model.add_transition(s_offer, s_happiness)
    model.bake()  # finalize the topology of the model
    print('The number of nodes:', model.node_count())
    print('The number of edges:', model.edge_count())
    print("Day 2 Example 3 Check: \na)")
    # P(r | s) and P(~r | s)
    print(model.predict_proba({'sun': 'sunny'})[1].parameters)
    # P(r | h, s) and P(~r | h, s)
    print("b)\n", model.predict_proba({'happiness': 'happy', 'sun': 'sunny'})[1].parameters)
    # P(r | h) and P(~r | h)
    print("c)\n", model.predict_proba({'happiness': 'happy'})[1].parameters)
    # P(r | h, ~s) and P(~r | h, ~s)
    print("d)\n", model.predict_proba({'happiness': 'happy', 'sun': 'not-sunny'})[1].parameters)


if __name__ == '__main__': main()