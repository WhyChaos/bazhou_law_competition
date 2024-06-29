from zhipuai import ZhipuAI
import json
from agent.base_agent import BaseAgent
import os



class SubCompanyInfoPlanAgent(BaseAgent):
    def __init__(self):
        super().__init__()


    def run(self, question):
        messages = []
        self.glm_run_record = 'sub_company_info_plan_table\n'

        messages.append({
            "role": "user",
            "content": '''现在有五个工具如下：
查子公司的工具：根据母公司名称获得所有子公司名称、数量和融资信息。
找母公司的工具：根据子公司名称获得母公司名称和融资信息。
筛选工具：根据融资信息的参股比例、投资金额进行筛选。
投资金额求和工具：根据融资信息的投资金额进行求和。
找最大的工具：根据融资信息的参股比例、投资金额找最大。

根据问题，告诉我回答这个问题依次要调用哪些工具。

输出字符串的列表。

例子1:
问题：我想知道北京当升材料科技股份有限公司控股超过半数、投资超5000万的子公司总共有多少家？
输出：["调用查子公司的工具：查询北京当升材料科技股份有限公司的所有子公司名称、数量和融资信息。", "调用筛选工具：根据参股比例字段筛选出50%以上的子公司名称、数量和融资信息。", "调用筛选工具：根据投资金额字段筛选出5000万以上的子公司名称、数量和融资信息。"]

例子2:
问题：金宏气体股份有限公司在子公司投资的总金额达到多少亿人民币？
输出：["调用查子公司的工具：查询金宏气体股份有限公司的所有子公司名称和融资信息。", "调用投资金额求和工具：根据投资金额字段求和。"]

例子3:
问题：请查询浙江古越龙山绍兴酒股份有限公司公司控股比例最高的子公司与其关系为何，投资的具体金额是多少，以及子公司总数量是多少？
输出：["调用查子公司的工具：查询浙江古越龙山绍兴酒股份有限公司的所有子公司名称和融资信息。", "调用找最大的工具：根据参股比例找最大。"]

例子4:
问题：福安药业旗下包含哪些子公司？
输出：["调用查子公司的工具：查询福安药业的所有子公司名称。"]

例子5:
问题：请问依米康软件技术（深圳）有限责任公司的上级控股企业是哪一家？他们对它的持股比例如何？他们总共控制几家下属公司？"
输出：["调用找母公司的工具：查询依米康软件技术（深圳）有限责任公司的母公司名称和融资信息。", "调用查子公司的工具：查询该母公司的所有子公司名称和数量。"]   

例子6:
问题：请告知我，上海百钠新能源科技有限公司、伊春碧水环保工程有限公司、浙江天能物联网科技有限公司分别隶属于哪家公司旗下子公司。
输出：["调用找母公司的工具：查询上海百钠新能源科技有限公司、伊春碧水环保工程有限公司、浙江天能物联网科技有限公司的母公司名称和融资信息。"]

问题：''' + question + '\n' +
'输出：'
        })
        while True:
            response = self.client.chat.completions.create(
                model=self.model_type,  # 填写需要调用的模型名称
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p
            )
            if response.choices[0].message.tool_calls is None:
                plan = response.choices[0].message.content
                self.glm_run_record += f'finish_reason:{response.choices[0].finish_reason};content:{response.choices[0].message.content}\n'
                try:
                    plan = json.loads(plan)
                    break
                except Exception as e:
                    print('Retry')
        return plan
