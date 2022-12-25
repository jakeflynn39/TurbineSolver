from re import L
from ssl import HAS_TLSv1_1


class Turbine:
    # A turbine is defined by it's q, w, h1, h2, and m
    m = 0 # Assumes mass flow rate does not come in to play
    
    # Calling turbine asks for an varible to solve for the asks for known variables
    def __init__(self, choice):
        self.choice = choice

        # If enthalpy is desired, need to find is mass flow rate is used
        if self.choice == "h1" or self.choice == "h2":
            self.answer = input("Do you know the mass flow rate?(y/n) ")
            while self.answer != "y" and self.answer != "n":
                self.answer = input("Please select y or n ")
            if self.answer == "y":
                self.m = Asker.ask_mass()

        # Asks for missing inputs depending on what desired variable is
        if self.choice != "h1":
            self.h1 = Asker.ask_h1()

        if self.choice != "h2":
            self.h2 = Asker.ask_h2()
        while self.choice != "h1" and self.choice != "h2":
            if self.h2 > self.h1: # Exit enthalpy cannot be greater than entry enthalpy
                print("Because we are operating in the conditions of a turbine, the exit enthalpy cannot be greater than the entry enthalpy.")
                self.h2 = Asker.ask_h2()
            else:
                break

        if self.choice == "W" or self.choice == "Q":
            self.m = Asker.ask_mass()

        # If Q or m is chosen, or if h1 or h2 is chosen and we know the mass flow rate
        if self.choice == "Q" or self.choice == "m" or (self.m != 0 and (choice == "h1" or choice == "h2")):
            self.W = Asker.ask_W()
        elif self.choice != "w" and self.choice != "W":
            self.w = Asker.ask_w()

        # If W or m is chosen, or if h1 or h2 is chosen and we know the mass flow rate 
        if self.choice == "W" or self.choice == "m" or (self.m != 0 and (choice == "h1" or choice == "h2")):
            self.Q = Asker.ask_Q()
        elif self.choice != "q" and self.choice != "Q":
            self.q = Asker.ask_q()

        # Calculates answers depending on inputs
        if self.choice == "h1":
            if self.m == 0:
                self.h1 = Calculator.h1_solver_no_mass(self.q, self.w, self.h2)
            else:
                self.h1 = Calculator.h1_solver_mass(self.Q, self.W, self.m, self.h2)
            print("The enthalpy into the system is {h1} kJ/kg.".format(h1 = self.h1))

        if self.choice == "h2":
            if self.m == 0:
                self.h2 = Calculator.h2_solver_no_mass(self.q, self.w, self.h1)
            else:
                self.h2 = Calculator.h2_solver_mass(self.Q, self.W, self.m, self.h1)
            print("The enthalpy out of the system is {h2} kJ/kg.".format(h2 = self.h2))

        if self.choice == "q":
            self.q = Calculator.q_solver(self.w, self.h1, self.h2)
            print("The specific heat transfer is {q} kJ/kg.".format(q = self.q))

        if self.choice == "w":
            self.w = Calculator.w_solver(self.q, self.h1, self.h2)
            print("The specific work done by the turbine is {w} kJ/kg.".format(w = self.w))

        if self.choice == "W":
            self.W = Calculator.W_solver(self.Q, self.m, self.h1, self.h2)
            print("The power outputted by the turbine is {W} kW.".format(W = self.W)) 
    
        if self.choice == "Q":
            self.Q = Calculator.Q_solver(self.W, self.m, self.h1, self.h2)
            print("The heat transfer rate is {Q} kW.".format(Q = self.Q))

        if self.choice == "m":
            self.m = Calculator.mass_solver(self.Q, self.W, self.h1, self.h2)
            print("The mass flow rate is {m} kg/s.".format(m = self.m))

class Calculator:
    # This class is used as a calculator
    def q_solver(w, h1, h2): # solves for q
        q = w + h2 - h1
        return q
    
    def w_solver(q, h1, h2):
        w = q + h1 - h2
        return w

    def h1_solver_no_mass(q, w, h2):
        h1 = w + h2 - q
        return h1
    
    def h2_solver_no_mass(q, w, h1):
        h2 = q - w + h1
        return h2
    
    def h1_solver_mass(Q, W, m, h2):
        h1 = (W - Q) / m + h2
        return h1

    def h2_solver_mass(Q, W, m, h1):
        h2 = (Q - W) / m + h1
        return h2

    def Q_solver(W, m, h1, h2):
        Q = W + m * (h2 - h1)
        return Q
    
    def W_solver(Q, m, h1, h2):
        W = Q + m * (h1 - h2)
        return W

    def mass_solver(Q, W, h1, h2):
        mass_flow_rate = (W - Q) / (h1 - h2)
        return mass_flow_rate

class Asker:
    # This class is used to ask for variables
    def ask_q():
        return float(input("What is the specific heat transfer, in kJ/kg? "))
    
    def ask_w():
        return float(input("What is the specific work done by the turbine, in kJ/kg? "))
    
    def ask_h1():
        return float(input("What is the enthalpy into the turbine, in kJ/kg? "))
    
    def ask_h2():
        return float(input("What is the enthalpy out of the turbine, in kJ/kg? "))
    
    def ask_mass():
        return float(input("What is the mass flow rate, in kg/s? "))

    def ask_Q():
        return float(input("What is the heat transfer, in kW? "))    

    def ask_W():
        return float(input("What is the work done by the turbine, in kW? "))

#Intro to the project
print("Welcome to the turbine solver. For this, we assume no change in kinetic or potential energy, steady state, and steady flow.")    

#Asking the user for the variable they want to solve for
solve_for = input("What would you like to solve for? ")
while solve_for != "w" and solve_for != "q" and solve_for != "W" and solve_for != "h1" and solve_for != "h2" and solve_for != "Q" and solve_for != "m":
    solve_for = input("None of those are variables that go into a turbine. Please select again. ")

Turbine(solve_for)
print("Congrats, you were able to solve this turbine!")