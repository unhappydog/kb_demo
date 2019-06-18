import ahocorasick


class ACLinker:
    def __init__(self, key_id):
        self.keys = key_id
        self.init()

    def init(self):
        self.automaton = ahocorasick.Automaton()
        for k, v in self.keys.items():
            self.automaton.add_word(k, (v, k))
        self.automaton.make_automaton()

    def link_text(self, text):
        """
        input is a text
        return is list of link tupe, where each link tupe is a 4 elements tupe
        (start, end, len, (_id, linked_text))
        :param text:
        :return:
        """
        if text is None:
            return ""
        text = text.lower()
        result = []
        final_result = []
        for end_index, (id, original_value) in self.automaton.iter(text):
            start_index = end_index - len(original_value) + 1
            assert text[start_index:start_index + len(original_value)] == original_value
            result.append((start_index, end_index, len(original_value), (id, original_value)))
        result = sorted(result, key=lambda x: x[2], reverse=True)
        for result_tupe in result:
            if self.is_good_result(result_tupe, final_result):
                final_result.append(result_tupe)
        return final_result

    def remove_over_lab(self, tupes1, tupes2):
        final_result = []
        result = tupes1 + tupes2
        for result_tupe in result:
            if self.is_good_result(result_tupe, final_result):
                final_result.append(result_tupe)
        return final_result

    def is_good_result(self, result_tupe, final_result):
        """
        如果该结果不和已知的结果中的每一个相交，那么这就是一个好的结果
        :param result_tupe:
        :param final_result:
        :return:
        """
        for final_result_tupe in final_result:
            if self.over_lap(result_tupe, final_result_tupe):
                return False
        return True

    def over_lap(self, a, b):
        """
        计算两个结果是否相交
        :param a:
        :param b:
        :return:
        """
        if a[0] > b[1] or a[1] < b[0]:
            return False
        else:
            return True


if __name__ == '__main__':
    map_dict = {
        'hello': 1,
        'bello': 2,
        'llo': 3
    }

    text = 'helow hellow hell bello hellowbello'
    aclinker = ACLinker(map_dict)
    print(aclinker.link_text(text))
