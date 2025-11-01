import os
import dotenv
import requests

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.tools import Tool
# from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def visit_recommender(city):
    """
    景点推荐
    :param city:
    :return:
    """
    VISIT_API_KEY = os.getenv('VISIT_API_KEY')
    VISIT_BASE_URL = os.getenv('VISIT_BASE_URL')

    parts = city.split(',')
    city = parts[0].strip()
    keyword = parts[1].strip() if len(parts) > 1 else "景点"
    params = {
        'city': city,
        'key': VISIT_API_KEY,
        'keywords': keyword,
        'types': '110000',
        'page': 1,
        'offset': '10',
        'extensions': 'all',
    }

    response = requests.get(VISIT_BASE_URL, params=params)
    data = response.json()

    if data['status'] == '1':
        points = data['pois']
        print(f"✅ 找到 {len(points)} 个景点\n")

        if keyword != "景点":
            result = f"为您推荐{city}的{keyword}相关景点：\n\n"
        else:
            result = f"为您推荐{city}的热门景点：\n\n"

        for i, points in enumerate(points, 1):
            result += f"{i}. {points['name']}\n"
            result += f"   地址：{points.get('address', '暂无信息')}\n\n"

        return result
    else:
        return f"未找到{city}的景点：{data.get('info', '未知错误')}"


# visit_tool = Tool(
#     func=visit_recommender,
#     name="visit_recommendation",
#     description="景点推荐",
# )
#
# llm = ChatOpenAI(model_name="gpt-4o-mini")
#
# prompt_template = ChatPromptTemplate.from_messages([
#     ("system",
#      """你是一个专业的旅行推荐助手，专门帮助用户推荐景点。
#
#      重要规则：
#      1. 当用户询问景点、旅游、游玩、去哪里玩时，调用visit_recommendation工具
#      2. 输入格式为：城市名称
#      3. 如果用户没有指定城市，请主动询问
#      4. 严格基于工具返回的景点信息进行推荐，不要编造或添加工具返回结果之外的景点
#      5. 如果工具返回的景点不理想，如实告诉用户并建议更具体的搜索条件
#
#      示例：
#      - 用户："北京有什么好玩的？" → "北京"
#      - 用户："推荐上海的历史景点" → "上海,历史"
#      - 用户："杭州西湖附近的景点" → "杭州,西湖"
#      """),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])
#
# agent = create_tool_calling_agent(
#     llm=llm,
#     prompt=prompt_template,
#     tools=[visit_tool],
# )
#
# agent_executor = AgentExecutor(
#     agent=agent,
#     tools=[visit_tool],
#     verbose=True,
#     memory=ConversationBufferMemory(),
# )
#
# user_input = input(f"请输入你的需求：")
# result_visit = agent_executor.invoke({"input": user_input})
#
# print(result_visit['output'])
#
