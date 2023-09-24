"""
Constructing the LMIS-LR algorithm from Algorithm 1
∆-approximation (where ∆ = maximum number of workers on the same task)
∆ = maxj=1,...,m |Nj (I)| (m = #of tasks, N = set of bidders who can contribute to task j.
∆ is upper bounded by n (number of total workers)
"""


class A:

    def __init__(self, bidding_profile, contribution, demand):
        """
        Constructor
        :param bidding_profile: b / = (c, I) - [c , [s, f]] // size n
        :param contribution: q / == r   // size n
        :param demand: d / size m
        """

        self.b_profile = bidding_profile
        self.contribution = contribution
        self.demand = demand

    @classmethod
    def calc_Q(cls, q, demand, t_instants):

        sum_q = [0] * len(demand)
        for j in range(1, len(demand) + 1):
            for x in range(len(t_instants)):
                if t_instants[x][0] <= j <= t_instants[x][1]:
                    sum_q[j - 1] += q[x]
        return sum_q

    @classmethod
    def calc_D(cls, Q, demand):
        D = [0] * len(demand)
        for i in range(len(Q)):
            D[i] = Q[i] - demand[i]
        return D

    def run(self):

        p = [0] * len(self.b_profile)
        T = [0] * len(self.b_profile)
        for i in range(len(self.b_profile)):
            p[i] = self.b_profile[i][0]
            T[i] = self.b_profile[i][1]

        Q = self.calc_Q(self.contribution, self.demand, T)
        r = self.contribution
        D = self.calc_D(Q, self.demand)

        J = []
        for i in range(1, len(self.contribution) + 1):
            J.append(i)

        m = len(self.demand)

        P2 = LMIS(p, T, r, D, J, m, self.demand)
        alg2_sol = P2.run()

        return alg2_sol


class LMIS:

    def __init__(self, penalty, intervals, activ_resour, avail_resour, set_activities, time_instants, upd_demand):
        """
        Constructor
        :param penalty: p /vector size n                       // p = [10,2,3]
        :param intervals: T /vector of intervals size n        // T = [[1,3], [2,4], [1,5]]
        :param activ_resour: r / vector                        // r = [5,7,8]
        :param avail_resour: D / vector size m                 // D = [15,12,18,20,11]
        :param set_activities: J / set (S)                     // J = {1,2,3}
        :param time_instants: m/ list of time instants         // m= {1,2,3,4,5}
        :param upd_demand: d
        """

        self.penalty = penalty
        self.intervals = intervals
        self.activ_resour = activ_resour
        self.avail_resour = avail_resour
        self.J = set_activities
        self.time_instants = time_instants
        self.upd_demand = upd_demand

    def calc_max_R(self, S):
        """
        R*(S,T,D)
        :return:
        """

        max_r = []
        for j in range(1, self.time_instants + 1):
            in_T = []
            for k in S:
                if self.intervals[k - 1][0] <= j <= self.intervals[k - 1][1]:
                    in_T.append(k - 1)

            ri = 0
            for x in in_T:
                ri += self.activ_resour[x]

            max_r.append(ri)

        for i in range(self.time_instants):
            max_r[i] = max_r[i] - self.avail_resour[i]

        self.set_t_max(max_r.index(max(max_r)) + 1)
        self.set_r_max(max(max_r))
        return max(max_r)

    def set_t_max(self, x):  # line 3
        self.t = x

    def get_t_max(self):  # line 3
        return self.t

    def set_min_j(self, x):  # line 7
        self.j = x

    def get_min_j(self):  # line 7
        return self.j

    def set_r_max(self, x):  # line 2
        self.r_max = x

    def get_r_max(self):  # line 2
        return self.r_max

    def run(self):
        """
        Algorithm Execution
        :return:
        """
        S = self.J.copy()  # line1

        k = 0  # line1
        pk = self.penalty.copy()
        selection_order = []
        while self.calc_max_R(S) > 0:  # line 2
            tmax = self.get_t_max()  # line 3
            Jt = []  # line 4
            for x in range(len(self.intervals)):  # line 4
                if self.intervals[x][0] <= tmax <= self.intervals[x][1]:  # line 4
                    Jt.append(x + 1)  # line 4

            Sk = [value for value in S if value in Jt]  # line 4

            ek = []  # line 5
            for i in Sk:  # line 5
                temp_R = self.get_r_max()  # line 5
                if temp_R < self.activ_resour[i - 1]:  # line 5
                    denominator = temp_R  # line 5
                else:  # line 5
                    denominator = self.activ_resour[i - 1]  # line 5
                ek.append(pk[i - 1] / denominator)  # line 5
            if ek:
                min_ek = min(ek)  # line 5
            else:
                return 0, 0, 0

            for i in range(len(ek)):
                if ek[i] == min_ek:
                    self.set_min_j(Sk[i])

            for i in range(1, self.time_instants + 1):  # line 6
                if i in Sk:  # line 6a
                    temp_R = self.get_r_max()  # line 6a
                    if temp_R < self.activ_resour[i - 1]:  # line 6a
                        denominator = temp_R  # line 6a
                    else:  # line 6a
                        denominator = self.activ_resour[i - 1]  # line 6a

                    pk[i - 1] = pk[i - 1] - min_ek * denominator  # line 6a

            j = self.get_min_j()  # line 7
            selection_order.append(j)
            S.remove(self.get_min_j())  # line 8

        initial_solution = []
        initial_cost = 0
        for i in self.J:
            if i not in S:
                initial_solution.append(i)

        for i in initial_solution:
            initial_cost += self.penalty[i - 1]

        final_solution = initial_solution.copy()

        # here starts the deletion
        S = []
        for i in range(1, len(self.J) + 1):
            if i not in initial_solution:
                S.append(i)

        for i in reversed(selection_order):

            S.append(i)

            final_solution.remove(i)

            if self.calc_max_R(S) > 0:
                final_solution.append(i)
                S.pop()

        final_solution.sort()

        final_cost = 0
        for j in final_solution:
            final_cost += self.penalty[j - 1]

        return selection_order, final_solution, final_cost
