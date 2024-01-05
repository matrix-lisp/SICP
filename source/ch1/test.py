def process():
    data_new = {}
    for line in file('data/en-country.data'):
        a = line.strip().split()
        if len(a) != 3:
            print line
            continue
        day, country, total = a
        data_new[day + ',' + country] = total

    data_ret = {}
    for line in file('data/en-country-ret.data'):
        a = line.strip().split()
        if len(a) != 3:
            print line
            continue
        day, country, total = a
        data_ret[day + ',' + country] = total

    f = file('en-Tue.csv', 'w')
    for k, dnu in data_new.iteritems():
        ret = data_ret.get(k)
        if ret is None:
            ret = '0'
        if int(dnu) < int(ret):
            print k
        line = k + ',' + dnu + ',' + ret
        f.write(line + '\n')
    f.close()


def process_all():
    data_new = {}
    for line in file('data/en-country.data'):
        a = line.strip().split()
        if len(a) != 3:
            print line
            continue
        day, country, total = a
        val = data_new.get(day)
        if val is None:
            data_new[day] = int(total)
        else:
            data_new[day] += int(total)

    data_ret = {}
    for line in file('data/en-country-ret.data'):
        a = line.strip().split()
        if len(a) != 3:
            print line
            continue
        day, country, total = a
        val = data_ret.get(day)
        if val is None:
            data_ret[day] = int(total)
        else:
            data_ret[day] += int(total)

    f = file('en-Tue-all.csv', 'w')
    for k, dnu in data_new.iteritems():
        ret = data_ret.get(k)
        if ret is None:
            ret = '0'
        if int(dnu) < int(ret):
            print k
        line = k + ',' + dnu + ',' + ret
        f.write(line + '\n')
    f.close()


def uuid_api_check():
    data = {}
    for line in file('data/data'):
        if line.find('WARN') >= 0:
            continue
        a = line.strip().split()
        if len(a) != 3:
            continue
        uuid, api, total = a
        val = data.get(uuid)
        if val is None:
            val = {api: total}
        else:
            val[api] = total
        data[uuid] = val

    check_api_list = ['/device/registration', '/version/sign']
    for uuid, val in data.iteritems():
        flag = True
        for api in val.keys():
            if api not in check_api_list:
                flag = False
                break
        if flag:
            print uuid, val


def af_article_process():
    # article_region_lines = [line.strip().split(',')
    #                        for line in file('AF-article-region-0104-0107.csv')]
    # article_all_lines = [line.strip().split(',')
    #                     for line in file('AF-article-all-0104-0107.csv')]
    article_uvpv_lines = [line.strip().split()
                          for line in file('af-article-uv-pv.data')
                          if line.find('WARN') < 0]
    article_push_lines = [line.strip().split()
                          for line in file('article-push.data')]

    article_lines = [line.strip().split(',') for line in file('AF-article-all-0104_0107.csv')]
    region_lines = [line.strip().split() for line in file('region.data')]

    # article_all_lines = [line.strip().split(',')
    #                     for line in file('af-article-push-stat.csv')]
    # article_uvpv_lines = [line.strip().split()
    #                      for line in file('af-article-id-uv-pv.data')
    #                      if line.find('WARN') < 0]

    #article_region = dict([(item[2], item[1]) for item in article_region_lines])
    article_region = dict([(item[0], item[1]) for item in region_lines])
    article_uvpv = dict([(item[0], item[1:]) for item in article_uvpv_lines])
    article_push = dict([(item[0], item[1]) for item in article_push_lines])

    for item in article_lines:
        article_id = item[2]
        region = article_region.get(article_id)
        if region is None:
            continue
        item[4] = '-'
        if region != '0':
            item[1] = region

        uvpv = article_uvpv.get(article_id)
        if uvpv is None:
            uvpv = ['0', '0']
        item += uvpv
        push_id = article_push.get(article_id)
        if push_id is None:
            push_id = 'push'
        item += [push_id]
        print ','.join(item)


def nginx_split(line):
    # find "..."
    idx = line.find('"')
    if idx >= 0:
        next_idx = line.find('"', idx + 1)
        # print line[:idx - 1], line[idx + 1:next_idx], line[next_idx + 1:]
        if idx == 0:
            array = []
        else:
            array = nginx_split(line[:idx - 1])
        return array + [line[idx + 1:next_idx]] + nginx_split(line[next_idx + 1:])

    # find [...]
    idx = line.find('[')
    if idx >= 0:
        next_idx = line.find(']', idx + 1)
        if idx == 0:
            array = []
        else:
            array = nginx_split(line[:idx - 1])
        return array + [line[idx + 1:next_idx]] + nginx_split(line[next_idx + 1:])

    # find \s
    return line.split()


def user_agent():
    d = {}
    for line in file('lost_user_agent.data'):
        if line.find('Mac OS X') > 0:
            try:
                key = line.split()[-2].split('/')[1]
            except IndexError:
                print line
                continue
        else:
            a = line[line.find('('): line.find(')')].split('; ')
            if len(a) > 3:
                key = a[-2]
                if key.find('Build') < 0:
                    key = a[-1]
            else:
                key = a[-1]
        if d.get(key) is None:
            d[key] = 1
        else:
            d[key] += 1

    f = file('lost_user_agent.csv', 'w')
    for k, v in d.iteritems():
        f.write(k + ',' + str(v) + '\n')
    f.close()

def matrix():
    s = 0.8
    e = 0.9
    d = 0.000001
    w = 1.13
    k = 6.5
    l = 11.0
    data = {}
    while s < e:
        s += d
        v = s/w + s/k + s/l
        data[s] = abs(1 - v)
    array = sorted(data.iteritems(), key=lambda d:d[1], reverse=True)
    for item in array:
        print item

if __name__ == '__main__':
    # process()
    # af_article_process()
    #line = '218.205.23.46 - http [02/Oct/2016:00:00:01 +0800] "GET /share/list/article/228891?size=40 HTTP/1.1" 200 96 0.128 "0.127" "https://api.dongqiudi.com/article/228891.html" "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A456 NewsApp/4.8.1 NetType/NA Technology/Wifi (iPhone; iOS 10.0.2; Scale/3.00) (modelIdentifier/iPhone8,2 )" "218.205.23.46" "@pl37kqCWDPI1vX5ytCw++FrTxLx9wRbDioFscj/xUk86wOQvD+Xcn6ZG6/0Yt1hYX+fMKjniQKw=" "kT06ztOl1VDyPCeyIvR4E4SoYnPPCeUe7IcmB5oYLux7gN276BOJ8Kt6leu60zUq" "zh-cn"'
    #array = nginx_split(line)
    # print len(array)
    # for item in array:
    #    print item
    # user_agent()
    matrix()
