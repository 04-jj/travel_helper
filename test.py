import requests


def search_beijing_attractions(keyword=None):
    """
    搜索北京景点
    keyword: 可选，搜索关键词，如"故宫"、"长城"等
    """
    VISIT_API_KEY = "b2e668aa1037bcf94816ec42e075c014"
    BASE_URL = "https://restapi.amap.com/v3/place/text"

    # 构建搜索参数
    params = {
        'key': VISIT_API_KEY,
        'city': '北京',
        'types': '110000',  # 景点类型编码
        'offset': '10',  # 返回10个结果
        'page': '1',
        'extensions': 'all'  # 返回详细信息
    }

    # 如果有关键词，添加到参数中
    if keyword:
        params['keywords'] = keyword
        print(f"🔍 正在搜索北京与'{keyword}'相关的景点...")
    else:
        print("🔍 正在搜索北京热门景点...")

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        print(f"📡 API响应状态: {data.get('status')}, 信息: {data.get('info')}")

        if data['status'] == '1' and data.get('pois'):
            pois = data['pois']
            print(f"✅ 找到 {len(pois)} 个景点\n")

            for i, poi in enumerate(pois, 1):
                print(f"{i}. 🏛️  {poi['name']}")
                print(f"   📍 地址：{poi.get('address', '暂无')}")
                print(f"   🏷️ 类型：{poi.get('type', '暂无')}")

                # 联系电话
                if poi.get('tel'):
                    print(f"   📞 电话：{poi['tel']}")

                # 评分和价格信息
                if 'biz_ext' in poi:
                    biz_ext = poi['biz_ext']
                    rating = biz_ext.get('rating', '')
                    cost = biz_ext.get('cost', '')
                    if rating:
                        print(f"   ⭐ 评分：{rating}/5")
                    if cost:
                        print(f"   💰 人均：{cost}元")

                # 坐标信息
                if 'location' in poi:
                    lon, lat = poi['location'].split(',')
                    print(f"   🗺️ 坐标：经度 {lon}, 纬度 {lat}")

                print()  # 空行分隔

            return len(pois)
        else:
            print(f"❌ 未找到景点信息：{data.get('info', '未知错误')}")
            return 0

    except Exception as e:
        print(f"❌ 搜索景点时出错：{str(e)}")
        return 0


def test_different_searches():
    """
    测试不同类型的搜索
    """
    print("=" * 60)
    print("🏞️ 北京景点搜索测试")
    print("=" * 60)

    # 测试1：搜索所有北京景点
    print("\n1. 北京所有景点搜索测试")
    print("-" * 30)
    count1 = search_beijing_attractions()

    # 测试2：搜索故宫相关景点
    print("\n2. 故宫相关景点搜索测试")
    print("-" * 30)
    count2 = search_beijing_attractions("故宫")

    # 测试3：搜索长城相关景点
    print("\n3. 长城相关景点搜索测试")
    print("-" * 30)
    count3 = search_beijing_attractions("长城")

    # 测试4：搜索公园类景点
    print("\n4. 公园类景点搜索测试")
    print("-" * 30)
    count4 = search_beijing_attractions("公园")

    # 测试5：搜索博物馆
    print("\n5. 博物馆搜索测试")
    print("-" * 30)
    count5 = search_beijing_attractions("博物馆")

    # 汇总结果
    print("=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    print(f"所有景点搜索：找到 {count1} 个结果")
    print(f"故宫相关搜索：找到 {count2} 个结果")
    print(f"长城相关搜索：找到 {count3} 个结果")
    print(f"公园类搜索：找到 {count4} 个结果")
    print(f"博物馆搜索：找到 {count5} 个结果")


def search_specific_attraction(attraction_name):
    """
    搜索特定景点详细信息
    """
    print(f"\n🔍 详细搜索：{attraction_name}")
    print("-" * 40)

    VISIT_API_KEY = "b2e668aa1037bcf94816ec42e075c014"
    BASE_URL = "https://restapi.amap.com/v3/place/text"

    params = {
        'key': VISIT_API_KEY,
        'city': '北京',
        'keywords': attraction_name,
        'types': '110000',
        'offset': '5',
        'extensions': 'all'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data['status'] == '1' and data.get('pois'):
            pois = data['pois']
            for poi in pois:
                if attraction_name in poi['name']:
                    print(f"🎯 找到目标：{poi['name']}")
                    print(f"📍 详细地址：{poi.get('address', '暂无')}")
                    print(f"🏷️ 分类标签：{poi.get('type', '暂无')}")

                    if poi.get('tel'):
                        print(f"📞 联系电话：{poi['tel']}")

                    # 商业扩展信息
                    if 'biz_ext' in poi:
                        biz_ext = poi['biz_ext']
                        print(f"⭐ 用户评分：{biz_ext.get('rating', '暂无')}")
                        print(f"💰 参考价格：{biz_ext.get('cost', '暂无')}元")
                        print(f"🍽️ 是否可订餐：{biz_ext.get('meal_ordering', '未知')}")

                    # 坐标信息
                    if 'location' in poi:
                        lon, lat = poi['location'].split(',')
                        print(f"🗺️ 精确坐标：经度 {lon}, 纬度 {lat}")

                    break
            else:
                print(f"未找到精确匹配 '{attraction_name}' 的景点")
        else:
            print(f"搜索失败：{data.get('info', '未知错误')}")

    except Exception as e:
        print(f"搜索出错：{str(e)}")


if __name__ == "__main__":
    # 运行综合测试
    test_different_searches()

    # 测试特定景点详细搜索
    print("\n" + "=" * 60)
    print("🎯 特定景点详细搜索测试")
    print("=" * 60)

    specific_attractions = ["故宫博物院", "八达岭长城", "颐和园", "天坛公园"]

    for attraction in specific_attractions:
        search_specific_attraction(attraction)
        print()