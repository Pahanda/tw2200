# Data structures for graphs, for use in game starmap.
# Based on code from here:
#  * https://www.python.org/doc/essays/graphs/
#  * https://www.python-course.eu/graphs_python.php
#  * https://gist.github.com/bwbaugh/4602818
#
# For the purposes of graph theory:
#  * node/vertex = system
#  * edge = hyperlane

import operator

class StarMap():
    def __init__(self, starmap={}):
        self.starmap = starmap

    # Find any isolated systems.
    def find_isolated(self):
        isolated = []
        for system, data in self.starmap.iteritems():
            if not data.connected:
                isolated.append(data.system_name)
        return isolated

    # Add a system (unconnected by default, can provide if desired).
    def add_system(self, system_name, connections=[]):
        if system_name not in self.starmap:
            self.starmap[system_name] = System(system_name, connections)

    # Add a bidirectional hyperlane between two systems (by name).
    def add_hyperlane(self, system1, system2):
        # Sanity checks.
        if system1 not in self.starmap or system2 not in self.starmap:
            return
        if system1 == system2:
            return

        if system1 not in self.starmap[system2].connected:
            self.starmap[system2].add_connection(system1)

        if system2 not in self.starmap[system1].connected:
            self.starmap[system1].add_connection(system2)

    # Finds all paths between two systems.
    def all_paths(self, s_start, s_end, path=[]):
        path = path + [s_start]
        if s_start == s_end:
            return [path]
        if s_start not in self.starmap:
            return None

        paths = []
        for system in self.starmap[s_start].connected:
            if system not in path:
                newpaths = self.all_paths(system, s_end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    # Finds the shortest path between two vertices.
    def shortest_path(self, s_start, s_end, path=[]):
        path = path + [s_start]
        if s_start == s_end:
            return path
        if s_start not in self.starmap:
            return None
        shortest = None
        for system in self.starmap[s_start].connected:
            if system not in path:
                newpath = self.shortest_path(system, s_end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def display(self):
        for system, data in self.starmap.iteritems():
            print '--'+data.system_name+'--\nConnections to:'
            print data.connected

class System:
    def __init__(self, system_name, adjacent=[]):
        self.connected = adjacent
        self.system_name = system_name

    def add_connection(self, system):
        # Apparently we have to force this assignment (instead of using an append()), even though we defined
        # our variable as an instance in __init__.  Whatever.
        if self.connected == []:
            self.connected = [system]
        else:
            self.connected += [system]

def test_map():
    map = StarMap()

    map.add_system('Sol')
    map.add_system('Alpha Centauri')
    map.add_system('Proxima Centauri')
    map.add_system('Betelgeuse')
    map.add_system('Orion')
    map.add_system('Cygnus X-1')

    map.add_hyperlane('Sol', 'Alpha Centauri')
    map.add_hyperlane('Sol', 'Betelgeuse')
    map.add_hyperlane('Alpha Centauri', 'Proxima Centauri')
    map.add_hyperlane('Betelgeuse', 'Orion')
    map.add_hyperlane('Proxima Centauri', 'Sol')

    return map

if __name__ == '__main__':
    starmap = test_map()

    print '== Map'
    starmap.display()

    print '== Isolated Systems'
    print starmap.find_isolated()

    print '== Shortest Path from Sol to Orion'
    print starmap.shortest_path('Sol', 'Orion')

    print '== All Paths from Proxima Centauri to Orion'
    print starmap.all_paths('Proxima Centauri', 'Orion')
