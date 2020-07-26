import os
from collections import defaultdict, OrderedDict
from copy import copy
from operator import itemgetter
from pprint import pprint

percentages = (0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.15,
               # 0.1, 0.05, 0.025, 0.01
               )


def make_dynamic_bookcase(elastic_ids=None):
    """

    :type elastic_ids: set of int
    :type companies: list of int
    """
    print('started')

    companies = []
    reverse_company_dict = {}
    i = 0
    with open('static_bookcases/companies.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                ss = line.split(',')
                companies.append(int(ss[1]))

                reverse_company_dict[int(ss[1])] = i
                i += 1

    if not elastic_ids:
        elastic_ids = set()
        with open('static_bookcases/temp_found_ids.txt', 'r') as f:
            line = f.read().strip().split(',')

            for item in line:
                try:
                    elastic_ids.add(reverse_company_dict[int(item)])
                except KeyError:
                    pass


    cliques = load_elastic_ids_cliques(elastic_ids)

    # save_updated_cliques(cliques)
    return get_bookcases(companies, cliques, percentages,
                  elastic_ids
                  )
    # main_2gis_inception(use_bookcase_info=False)
    #
    # for percentage in percentages:
    #     for file_name in files_to_delete:
    #         unlink(f'{output_path}/{percentage}/{file_name}')


# def save_updated_cliques(cliques):
#     with open(os.path.join(output_path, 'cluqies.txt'), 'w') as f:
#         for c in cliques:
#             a = list(c)
#             f.write(' '.join(a) + '\n')
#


def load_elastic_ids_cliques(elastic_ids):
    # print(elastic_ids)
    cliques = []
    with open('static_bookcases/cliques.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                ss = set([int(item) for item in line.split(' ')])
                found_ids = ss.intersection(elastic_ids)

                if found_ids:
                    cliques.append((ss, len(found_ids)))

    cliques.sort(key=lambda x: x[1] + len(x[0]) / 100,
                 reverse=True)
    # print(len(cliques))
    return [item[0] for item in cliques]


def get_bookcases(companies, cliques, percentages, elastic_ids=None):
    """
    От самого большого подграфа к самому малому, компании присваивается 2, если она впервые встречается и 1 если она уже встречалась в предыдущих подграфах
    Первый подграф сразу отправляется в новый шкаф.
    Далее идут следующие фильтры:
    1. если подграф полностью вторичен (состоит только из 1), то он не учитывается
    2. Если компании в подграфе на 30% совпадают с первым подграфом в шкафу, то они отправляются в этот шкаф, иначе для подграфа создается новый шкаф
    Важно отметить что подграф может быть отправлен в несколько уже созданных шкафов
    3. подграф отправляется в шкаф с дополнительным параметром R, который вычисляется относительно первого подграфа в шкафу
    R =(max+min)*max/min
    Где Max = Количество общих вершин / больший из двух подграфов * 100
    Min =  Количество общих вершин / меньший из двух подграфов * 100
    У первого подграфа R = 0

    Для каждой компании Находим в скольких шкафах она присутствует  с «2" и сохраняем эту информацию в 'companies_in_shelves.csv'

    Сохраняем таблицу shelves.csv
    ['# шкаф', номер элемента в шкафу', 'параметр R для подграфа', количество вторичных компаний подграфа, количество первичных компаний, общее количество компаний', весь граф целиком]

    Для каждого шкафа создаем три массива:
    0. уникальный список всех компаний внутри шкафа
    1. только вторичные компании в шкафу
    2. только первичные компании в шкафу

    Далее при сравнении шкафов, по парно сравниваем эти массивы
    И вычисляем R
    R =(max+min)*max/min
    Где Max = Количество общих вершин / больший из двух подграфов * 100
    Min =  Количество общих вершин / меньший из двух подграфов * 100
    Всю эту информацию сохраняем в bookcases_relations.csv
    """

    cliques_2 = get_twos_with_elastic(cliques, elastic_ids)

    """
    cliques_2 = [{'company_id': 1 or 2, ...} for each subgraph]
    """

    # with open(os.path.join(output_path, 'cluqies_twos.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    #     q = ['id', 'l1', 'l2', 'lo', 'система']
    #     f.write(';'.join(q) + '\r\n')
    #     for id, cliqu in cliques_2.items():
    #         if count_twos(cliqu) == 0:
    #             continue
    #         companies_count_in_subgraph = len(cliqu)
    #         primary_companies_count_in_subgraph = count_twos(cliqu)
    #         secondary_companies_count_in_subgraph = companies_count_in_subgraph - primary_companies_count_in_subgraph
    #         q = [str(id), str(secondary_companies_count_in_subgraph), str(primary_companies_count_in_subgraph),
    #              str(companies_count_in_subgraph), cliqu_to_str(cliqu)]
    #         f.write(';'.join(q) + '\r\n')
    # cycles_concats_data = []
    # cliques_2 = OrderedDict(sorted(cliques_2.items(), reverse=True, key=lambda x: len(x[1])))
    # print(len(cliques_2))
    dynamic_bookcase_data = []
    # companies_bookcase_history = defaultdict(dict)
    # save_bookcase_history(companies_bookcase_history, cliques_2, 1)
    for percentage in percentages:
        cliques_2, cycles_done, concats_made = allocate_cliques_recursive(cliques_2, percentage)

        # save_bookcase_history(companies_bookcase_history, cliques_2, percentage)
        # cycles_concats_data.append({'percentage': percentage,
        #                             'cycles_done': cycles_done,
        #                             'concats_made': concats_made})
        pprint(cliques_2)
        clique_with_elastic_ids = {}
        for clique_id, clique_items in cliques_2.items():
            ids_from_elastic = {}
            for company_id, one_two in clique_items.items():
                ids_from_elastic[companies[company_id-1]] = one_two
            clique_with_elastic_ids[clique_id] = ids_from_elastic

        dynamic_bookcase_data.append({'percentage': percentage,
                                      'bookcases': clique_with_elastic_ids,
                                      'concats_made': concats_made,
                                      'cycles_done': cycles_done, })

    return dynamic_bookcase_data
        # save_intermedia_bookcase_files_2(cliques_2, f'{output_path}/{percentage}')
        # main_2gis_inception(bookcase_path=f'{output_path}/{percentage}', use_bookcase_info=True)

    # with open(os.path.join(output_path, 'cycles_concats_data.csv'), 'w') as extended:
    #     writer = DictWriter(extended,
    #                         fieldnames=[
    #                             'percentage', 'cycles_done', 'concats_made'
    #                         ],
    #                         delimiter=';')
    #
    #     writer.writeheader()
    #     for data in cycles_concats_data:
    #         writer.writerow(data)

    # with open(os.path.join(output_path, 'companies_bookcase_history.csv'), 'w', encoding='utf-8-sig', newline='') as extended:
    #     writer = DictWriter(extended,
    #                         fieldnames=[
    #                             'company_id',
    #                         ] + [1,]+ [percentage for percentage in percentages],
    #                         delimiter=';')
    #
    #     writer.writeheader()
    #
    #     for company_id, history_data in companies_bookcase_history.items():
    #         history_data.update({'company_id': company_id})
    #         writer.writerow(history_data)


def save_intermedia_bookcase_files_2(cliques_2, output_path):
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'shelves.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        q = ['# шкаф', 'l1', 'l2', 'lo', 'система']
        f.write(';'.join(q) + '\r\n')
        for first_bookcase_index, clique in cliques_2.items():
            # bookcase = bookcases[first_bookcase_index]
            # for subgraph_index in range(len(bookcase)):
            cliqu = clique
            companies_count_in_subgraph = len(cliqu)
            primary_companies_count_in_subgraph = count_twos(cliqu)
            secondary_companies_count_in_subgraph = companies_count_in_subgraph - primary_companies_count_in_subgraph
            q = [str(first_bookcase_index),
                 str(secondary_companies_count_in_subgraph), str(primary_companies_count_in_subgraph),
                 str(companies_count_in_subgraph), cliqu_to_str(cliqu)]
            f.write(';'.join(q) + '\r\n')

    print('saved shelves.csv')


def get_clique_similarity(first_clique, second_clique):
    matched_companies_count = 0
    for c in second_clique:
        if second_clique[c] == '1':
            if c in first_clique:
                matched_companies_count += 1

    return matched_companies_count / len(first_clique)


def allocate_cliques_recursive(cliques_2, percentage=0.9):
    similarities_found = True
    cycles_done = 0
    concats_made = 0
    while similarities_found:
        similarities_found = False

        similarities = defaultdict(dict)
        for first_index, first_clique in cliques_2.items():
            # for first_index in range(len(cliques_2)):
            for second_index, second_clique in cliques_2.items():
                if second_index <= first_index:
                    continue
                # for second_index in range(1, len(cliques_2) - first_index):

                similarity = get_clique_similarity(first_clique, second_clique)
                if similarity > 0:
                    similarities[first_index][second_index] = similarity

        result = dict()
        used_indexes = set()
        # i = 0
        # for first_index in range(len(cliques_2)):
        for first_index, main_clique in cliques_2.items():

            # i += 1

            if first_index in used_indexes:
                continue
            nothing_to_concat = True
            for second_index, similarity in sorted(similarities.get(first_index, {}).items(), reverse=True,
                                                   key=itemgetter(1)):
                if similarity < percentage:
                    break
                if second_index in used_indexes:
                    continue
                second_similarities = similarities.get(second_index, None)
                if second_similarities is not None:
                    if similarity < max(second_similarities.values()):
                        continue
                nothing_to_concat = False
                similarities_found = True
                concats_made += 1
                used_indexes.update([first_index, second_index])
                new_dict = dict(cliques_2[second_index])
                for company_id, one_or_two in main_clique.items():
                    if company_id in new_dict.keys():
                        if one_or_two == '2':
                            new_dict.update({company_id: one_or_two})
                    else:
                        new_dict.update({company_id: one_or_two})

                result[first_index] = copy(new_dict)
                break
            if nothing_to_concat:
                used_indexes.add(first_index)
                result[first_index] = copy(main_clique)
                # result.append(dict(cliques_2[first_index]))
        if similarities_found:
            cycles_done += 1
        del cliques_2

        # cliques_2 = sorted(result, reverse=True, key=len)
        cliques_2 = OrderedDict(sorted(result.items(), reverse=True, key=lambda x: len(x[1])))

        # cliques_2 = result

        del result
    # print('cycles', cycles_done)
    # print('concats', concats_made, 'percentage', percentage)

    return cliques_2, cycles_done, concats_made


def get_twos_with_elastic(cliques, elastic_ids):
    cliques_2 = {}
    counted_companies = set()
    index_of_clique = 0
    for cliq in cliques:
        a = {}
        # cliq = sorted(cliq, reverse=True, key=int)
        found_two = False
        for c in cliq:
            if c not in elastic_ids:
                a[c] = '1'
            elif c in counted_companies:
                a[c] = '1'
            else:
                a[c] = '2'
                found_two = True
                counted_companies.add(c)
        if found_two:
            cliques_2[index_of_clique] = a
        index_of_clique += 1
    print('counted companies', len(counted_companies))
    # cliques_2.sort(key=count_twos, reverse=True)

    return cliques_2


def save_bookcase_history(companies_bookcase_history, cliques_2, percentage):
    for clique_index, clique in cliques_2.items():
        for company_id, one_or_two in clique.items():
            if one_or_two == '2':
                companies_bookcase_history[company_id].update({percentage: clique_index})


def count_twos(subgraph):
    n = 0
    for company_id in subgraph:
        if subgraph[company_id] == '2':
            n += 1
    return n


def cliqu_to_str(cliqu):
    a = []
    keys = list(cliqu.keys())
    keys.sort(key=int)
    for c in keys:
        a.append(str(c) + '(' + cliqu[c] + ')')
    return ' '.join(a)


if __name__ == '__main__':
    # load_elastic_ids_cliques()
    pprint(make_dynamic_bookcase())
