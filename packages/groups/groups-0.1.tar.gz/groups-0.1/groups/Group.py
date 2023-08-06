from itertools import combinations

class Group:
    
    def __init__(self, set, func) -> None:
        self.set = set
        self.func = func

    def __eq__(self, other) -> bool:
        equal = True
        for a in self.set:
            if(self.func(a, a) != other.func(a, a)):
                equal = False
        if(self.set == other.set and equal):
            return True
        
        return False


    def __neq__(self, other) -> bool:
        equal = True
        for a in self.set:
            if(self.func(a, a) != other.func(a, a)):
                equal = False
        return (self.set != other.set or not equal)

    def is_associative(self) -> int:
        """returns 1 is group is asociative, 0 otherwise"""

        for a in self.set:
            for b in self.set:
                ab = self.func(a, b)
                for c in self.set:
                    bc = self.func(b, c)
                    a_bc = self.func(a, bc)
                    ab_c = self.func(ab, c)
                    if(a_bc != ab_c):
                        return 0
        return 1

    def is_closed(self) -> int:
        """returns 1 is group os closed, 0 otherwise"""

        for a in self.set:
            for b in self.set:
                ab = self.func(a, b)
                if(ab not in self.set):
                    return 0
        return 1

    def has_identity(self) -> int:
        """returns 1 is group has a unique identity, 0 otherwise"""

        identity_count = 0
        for a in self.set:
            is_identity = 1
            for b in self.set:
                ab = self.func(a, b)
                if(ab != b):
                    is_identity = 0
            if(is_identity == 1):
                identity_count += 1
        
        if(identity_count == 1):
            return 1
        else:
            return 0

    
    def identity(self) -> int:
        """returns the identity if group contains one, 0 otherwise"""

        for a in self.set:
            is_identity = 1
            for b in self.set:
                ab = self.func(a, b)
                if(ab != b):
                    is_identity = 0

            if(is_identity == 1):
                return a
        return 0

    
    def has_inverses(self) -> int:
        """returns 1 if group has inverses, 0 otherwise"""

        if(self.has_identity()):
            identity = self.identity()

            for a in self.set:
                has_inverse = 0
                for b in self.set:
                    ab = self.func(a, b)
                    if(ab == identity):
                        has_inverse = 1
                if(not has_inverse):
                    return 0
        return 1


    def inverse(self, elem):
        """Document this later"""
        
        if(self.has_inverses()):
            identity = self.identity()
            if(elem == identity):
                return identity
            else:
                for a in self.set:
                    if(self.func(elem, a) == identity):
                        return a
            


    def is_group(self) -> int:
        """checks if the set is a group, if true returns 1, otherwise 0"""

        if(not self.is_closed()):
            return 0
        if(not self.is_associative()):
            return 0
        if(not self.has_identity()):
            return 0
        if(not self.has_inverses()):
            return 0
        
        return 1

    def is_abelian(self) -> int:
        """checks if the group is abelian, returns 1 if true, otherwise 0"""

        for a in self.set:
            for b in self.set:
                ab = self.func(a, b)
                ba = self.func(b, a)
                if(ab != ba):
                    return 0
        return 1


    def is_subset(self, G) -> int:
        """checks if a set is a subset of the group, returns 1 if true, 0 otherwise"""

        for elem in self.set:
            if(elem not in G.set):
                return 0
        return 1

    def is_subgroup(self, G) -> int:
        """checks if a subset is a subgroup, returns 1 if true, 0 otherwise"""

        if(self.is_subset(G) and self.is_group()):
            return 1
        
        return 0

    def power(self, elem, pow: int):
        """computes the power of an element, using the user defined function
            returns the element to the given power
        """

        if(pow == 0):
            return self.identity()
        elif(pow == 1):
            return elem
        else:
            power_elem = elem
            for _ in range(2, pow+1):
                power_elem = self.func(power_elem, elem)
            return power_elem
        

    def subsets(self) -> list:
        """creates all subsets of the group, and returns them in a list"""

        size = len(self.set)
        combs = []
        for k in range(1, size):
            combs.append(list(combinations(self.set, k)))

        flat_combs = []
        for lst in combs:
            for combination in lst:
                flat_combs.append(list(combination))
        return flat_combs

    
    def subgroups(self) -> list:
        """finds all subgroups of the group, and returns them in a list"""

        subsets = self.subsets()
        subgroup_list = []
        for subset in subsets:
            H = Group(subset, self.func)
            subgroup_list.append(H)

        real_subgroups = []
        for subgroup in subgroup_list:
            if(subgroup.is_group()):
                real_subgroups.append(subgroup)

        return real_subgroups


    def left_coset(self, H, a):
        """parameters are a subgroup and an element and 
            the functions returns the left coset of H cnotaining a
        """

        if(H.is_group() and H.is_subgroup(self)):
            coset = []
            for x in H.set:
                coset.append(self.func(a, x))

            return Group(coset, self.func)

    
    def right_coset(self, H, a):
        """parameters are a subgroup and an element and 
            the functions returns the right coset of H cnotaining a
        """

        if(H.is_group() and H.is_subgroup(self)):
            coset = []
            for x in H.set:
                coset.append(self.func(x, a))

            return Group(coset, self.func)


    def is_normal(self, H) -> int:
        """checks if the right coset is equal to the left coset for all elements of the group
            returns 1 if true, 0 otherwise
        """

        for a in self.set:
            if(self.right_coset(H, a) != self.left_coset(H, a)):
                return 0
        return 1

    def normal_subgroups(self):
        """returns a list of all normal subgroups"""

        subgroups = self.subgroups()
        normal_subgroups = []
        for group in subgroups:
            if(self.is_normal(group)):
                normal_subgroups.append(group)

        return normal_subgroups

    def order(self, elem) -> int:
        """computes the order of a given elemen and returns an integer"""

        counter = 1
        computed_elem = elem
        if(elem == self.identity()):
            return 1
        while(computed_elem != self.identity()):
            computed_elem = self.func(computed_elem, elem)
            counter += 1

        return counter


    def group_generated_by(self, elem):
        """returns the group generated by an element"""

        group_set = [elem]
        if(elem == self.identity()):\
            return Group([self.identity()], self.func)

        computed_elem = elem
        counter = 1
        while(counter != self.order(elem)):
            computed_elem = self.func(computed_elem, elem)
            group_set.append(computed_elem)
            counter += 1
        group_set.sort()

        return Group(group_set, self.func)

    def is_cylic(self) -> int:
        """checks if the group is cyclic, returns 1 is yes, otherwise 0"""

        for elem in self.set:
            g = self.group_generated_by(elem)
            if(g == self):
                return 1
        return 0

    def get_generators(self) -> list:
        """gets the generators of the group and returns them as a list"""
       
        generators = []
        for elem in self.set:
            if(self.group_generated_by(elem) == self):
                generators.append(elem)

        return generators

    def pairs(self, H):
        pairs = []
        for a in self.set:
            for b in H.set:
                pairs.append((a, b))

        return pairs

    def external_direct_product(self, H):
        pairs = self.pairs(H)
        function = lambda x, y: (self.func(x[0], y[0]), H.func(x[1], y[1]))
        return Group(pairs, function)

    