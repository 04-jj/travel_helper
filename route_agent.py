import os
import dotenv
import requests
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.tools import Tool
# from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def geocode_address(address):
    """
    获取起点和终点的经纬度
    """
    GEOCODE_API_KEY = os.getenv('GEOCODE_API_KEY')
    GEOCODE_BASE_URL = os.getenv('GEOCODE_BASE_URL')
    params = {
        'q': address,
        'api_key': GEOCODE_API_KEY,
    }

    response = requests.get(GEOCODE_BASE_URL, params=params)
    data = response.json()

    if data and len(data) > 0:
        location = f"{data[0]['lon']},{data[0]['lat']}"
        return location
    else:
        return None


def route_planning(route_query):
    """
    使用高德API进行路径规划
    """
    ROUTE_API_KEY = os.getenv('ROUTE_API_KEY')
    ROUTE_BASE_URL = os.getenv('ROUTE_BASE_URL')

    points = route_query.split(',')
    if len(points) < 2:
        return "请提供起点和终点，格式：起点，终点"

    start_address = points[0].strip()
    end_address = points[1].strip()

    print(f"正在查询起点：{start_address}")
    print(f"正在查询终点：{end_address}")

    start_location = geocode_address(start_address)
    end_location = geocode_address(end_address)

    print(f"起点的经纬度：{start_location}")
    print(f"终点的经纬度：{end_location}")

    if not start_location:
        return f"无法找到起点 '{start_address}' 的坐标，请检查地址是否正确"
    if not end_location:
        return f"无法找到终点 '{end_address}' 的坐标，请检查地址是否正确"

    params = {
        'key': ROUTE_API_KEY,
        'origin': start_location,
        'destination': end_location,
        'strategy': 0,
        'extensions': 'all',
    }

    print("调用高德API...")
    response = requests.get(ROUTE_BASE_URL, params=params)
    data = response.json()

    print(f"高德API响应状态: {data.get('status')}, 信息: {data.get('info')}")

    if data['status'] == '1':
        route = data['route']
        path = route['paths'][0]

        # 构建详细结果
        result = f"🚗 路线规划完成：{start_address} → {end_address}\n\n"
        result += f"📊 总览：\n"
        result += f"📏 总距离：{int(path['distance']) / 1000:.1f}公里\n"
        result += f"⏱️ 预计时间：{int(path['duration']) / 60:.1f}分钟\n"
        result += f"🗺️ 详细路线（共{len(path['steps'])}步）：\n"

        steps = path['steps']
        for i, step in enumerate(steps, 1):
            instruction = step['instruction']
            instruction = instruction.replace('<b>', '').replace('</b>', '').replace('&nbsp;', ' ')
            distance = f"{int(step['distance']) / 1000:.1f}公里" if int(
                step['distance']) >= 1000 else f"{step['distance']}米"

            result += f"{i},{instruction},{distance}\n"

        return result
    else:
        return f"路径规划错误：{data.get('info', '未知错误')}"

#
# route_tools = Tool(
#     func=route_planning,
#     name="route_planning",
#     description="使用高德地图进行驾车路径规划"
# )
#
# # 获取大语言模型
# llm = ChatOpenAI(model_name="gpt-4o-mini")
#
# # 提示词
# prompt_template = ChatPromptTemplate.from_messages([
#     ("system",
#      "你是一个路径规划助手，帮助用户规划驾车路线。当用户询问路线时，调用route_planning工具，输入格式为：起点地址,终点地址"),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])
#
# agent = create_tool_calling_agent(
#     llm=llm,
#     prompt=prompt_template,
#     tools=[route_tools],
# )
#
# memory = ConversationBufferMemory()
#
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[route_tools],
#     verbose=True,
#     memory=memory,
# )
#
# user_input = input("请输入你的需求：")
# result_route = agent_executor.invoke({"input": user_input})
# print(result_route)
