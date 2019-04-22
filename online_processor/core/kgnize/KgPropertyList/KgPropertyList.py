class KgPropertyList:
    def __init__(self):
        self.property_list = []
        self.id_table = {}
        self.count = 0

    def push_property(self, name):
        self.id_table[self.count] = name
        self.count += 1
        return self.count - 1

    def push_path(self, id, par_id, path_name, pop_info):
        self.property_list.append((id, par_id, path_name, pop_info))


