# Lab Test Record Tracker — 面试准备手册

> 用途:以「面试官视角」吃透本项目,覆盖高频深挖题、示范回答、红区软肋话术。
> 定位:这是为 **UL Solutions(苏州)Software Engineer 岗(Job 9697,实验室运营数字化)** 做的技术对齐作品集项目。
> 性质:**personal portfolio / learning project,非雇佣工作**。放简历 Projects 区,标注清楚,不要塞进 2024 就业经历。

---

## 一、一句话定位(向面试官介绍本项目)

「这是为 UL 苏州岗做的全栈演示项目,主题是实验室测试记录管理,技术栈完全对齐 JD:Python(FastAPI)后端 + Vue3/TypeScript 前端 + Docker 多阶段构建 + Azure App Service 部署 + Azure DevOps CI/CD。我之前在 AspenTech 做的是工业软件 B 端(C# 栈),和 UL 同属工业领域;这个岗位要 Python 全栈,所以我用这个项目把 JD 列的技术栈端到端走了一遍,证明我能补齐栈的差异。它也是我健康恢复后系统学习的作品集。」

---

## 二、技术栈 ↔ UL JD 映射表

| JD 要求 | 本项目对应实现 |
|---|---|
| Python backend (Django/Flask/FastAPI) | FastAPI + SQLAlchemy + SQLite |
| Modern JS framework (Vue/React/Angular) | Vue 3 + TypeScript + Vite |
| TypeScript | 前端 `api.ts` / `App.vue` `<script setup lang="ts">` |
| Docker containers | 多阶段 `Dockerfile` + `docker-compose.yml` |
| Cloud (Azure/AWS) | Azure App Service (Linux) 部署 |
| Azure DevOps / Agile | `azure-pipelines.yml` + repo |
| Cross-functional / lab domain | 测试记录领域模型 |

---

## 三、面试考点地图(8 维度)

| 维度 | 代表问题 |
|---|---|
| 动机·契合 | 为何做此项目?与空窗叙事如何自洽?对应 JD 哪几条? |
| 架构 | 为何单容器托管前后端?一体 vs 前后端分离? |
| 后端逻辑 | 分页/部分更新如何实现?Pydantic 作用? |
| 数据建模 | TestRecord 字段为何这样设计?SQLite 为何能换 Postgres? |
| 前端 | Seed 5000 行前端如何渲染?搜索为何没加 debounce? |
| 容器化 | Docker 多阶段构建做什么?如何控镜像体积? |
| 云部署 | Azure CI/CD 流程?ACR 作用? |
| 安全·生产 | CORS 全开隐患?无认证/无测试怎么补? |

**红区(最易被深挖的薄弱点)**:无认证鉴权 · 无单元测试 · `created_at` 用 naive UTC · 搜索无防抖。

---

## 四、高频深挖题 + 示范回答(均基于真实代码)

### 1. 动机与契合
**Q:为什么做这个项目?和你的经历什么关系?**
A:见「一、一句话定位」。核心是:工业领域同源(AspenTech→UL)+ 栈差异(Python)用本项目补齐 + 健康恢复后的系统学习作品。

**Q:对应 JD 哪几条?**
A:背「二、映射表」。重点强调 Python 后端、Vue+TS、Docker、Azure、Azure DevOps 五条都端到端落地了。

### 2. 架构
**Q:为什么前后端打进一个容器,而不是分开部署?**
A:这是刻意的 single-container 模式——`main.py` 用 `StaticFiles` 把构建好的 `dist/` 挂到根路径,API 在 `/api` 下。对演示项目部署简单(一个镜像跑全栈)、适配 Azure App Service 单实例;若要更大规模,会拆成独立前端静态托管 + 后端服务 + 反向代理,README 已标注这是 demo 取舍。

### 3. 后端逻辑
**Q:分页怎么做的?部分更新怎么实现?**
A:列表用 `offset(skip).limit(limit)` 服务端分页,前端每页取 20 条(`crud.py` 的 `get_records`);部分更新用 Pydantic 的 `model_dump(exclude_unset=True)`,只把前端实际传的字段 `setattr` 进去,没传的不动——所以 `TestRecordUpdate` 全字段 Optional。

**Q:Pydantic 在这里干嘛?**
A:两层:入参校验(`TestRecordCreate` 必填 `sample_id`/`test_name`)+ 出参序列化(`TestRecordOut` 用 `from_attributes` 把 ORM 对象转 dict)。把「请求/响应长什么样」显式声明,省掉手写校验。

### 4. 数据建模
**Q:TestRecord 字段为何这样设计?**
A:核心字段 `sample_id`(样品编号,加 index 便于检索)、`test_name`、`operator`、`equipment`、`result_value`(Float)、`unit`、`status`(pending|pass|fail,默认 pending)、`note`、`created_at`(默认 utcnow)。覆盖了实验室测试记录的关键属性:谁测的、用什么设备、结果值、结论状态。

**Q:SQLite 为何能平滑换 Postgres?**
A:SQLAlchemy ORM 屏蔽了数据库差异;切换只需改 `database.py` 里的 `SQLALCHEMY_DATABASE_URL`(如 `postgresql+psycopg2://...`),`check_same_thread` 参数是 SQLite 专属、换库时去掉即可。生产用 Postgres 获得并发与约束能力。

### 5. 前端
**Q:Seed 5000 行前端怎么不卡?**
A:没全量渲染——前端 `limit=20` 只取一页,`v-for` 只渲染 20 行,点 Next 走 `skip+=20` 再拉。5000 是库里的量,不是 DOM 里的量。这正是 AspenTech「几十万行表格性能优化」的思路:服务端分页 + 按需取数。

**Q:搜索为什么没加 debounce?**
A(诚实):这是 demo 简化,每次 `@input` 都打 API。生产会加 300ms 防抖 + 给 `keyword` 加数据库索引;现在 SQLite 下量小无所谓,但我主动提这点,说明我知道代价。**(知道不完善、知道怎么补 = 加分)**

### 6. 容器化
**Q:Docker 多阶段构建做什么?镜像体积怎么控?**
A:Stage1 用 `node:20-alpine` 只负责 `npm run build` 出 `dist`;Stage2 用 `python:3.12-slim` 只拷后端代码 + 前端 `dist`,最终镜像不含 Node 和源码构建链,体积小、攻击面小。

### 7. 云部署
**Q:Azure CI/CD 流程?**
A:push 到 `main` → `azure-pipelines.yml` 用 `Docker@2` 把镜像 build 并 push 到 ACR → `AzureWebAppContainer` 把镜像拉到 App Service(Linux)部署。ACR 是私有镜像仓库,相当于中间枢纽。也可用 `deploy-azure.sh`(`az acr build` + `az webapp create`)手动部署。

### 8. 安全·生产(红区)
见「五、红区软肋与应对话术」。

---

## 五、红区软肋与应对话术(诚实 + 成长型,不辩解)

| 薄弱点 | 面试官可能的质疑 | 推荐话术 |
|---|---|---|
| CORS 全开 `*` | 任意域名都能调你的 API? | demo 为了方便;生产收成具体前端域名 + 加认证(JWT/OAuth)。 |
| 无认证/无测试 | 任何人都能增删数据?质量怎么保证? | 这是 portfolio 项目,没做鉴权和单测;若上生产,第一步加 Auth,用 pytest 给 CRUD/分页补集成测试。我清楚它现在不是生产级。 |
| `created_at` 用 `datetime.utcnow`(naive UTC) | 时区怎么处理? | 存的是无时区 UTC,展示端按用户时区转换;生产用 `datetime.now(timezone.utc)` 存 aware 时间,避免歧义。 |
| 搜索无防抖 | 输入每个字符都打 API? | demo 简化;生产加 300ms 防抖 + 数据库索引。 |
| `update` 接口写了、前端没接按钮 | 这个 PUT 接口为什么前端没用? | 接口(`/api/records/{id}` PUT)和 `updateRecord` 前端函数都齐,UI 编辑弹窗留作待补;实现路径清楚,补一个弹窗即可。 |

**原则**:被问到不足时,用「我知道它现在这样、我知道怎么补」的句式,展现工程判断力,而非 defensive 辩解。

---

## 六、现场演示验证清单(面试可能让你跑/看)

1. 起服务:`docker compose up --build`(或本地 `uvicorn backend.app.main:app --port 8000`)
2. 开 `http://localhost:8000` → 看到实验室记录管理页
3. 点 **Seed 5,000 rows** → 表格出现数据(验证前后端+DB 打通)
4. 开 `http://localhost:8000/docs` → FastAPI Swagger 接口文档(演示加分)
5. 验证 `/api/health` 返回 `{"status":"ok"}`
6. 有 GitHub 仓库时,展示仓库链接 + README

> 国内首次 `docker build` 若卡在 `load metadata for docker.io/...`,是连不上 Docker Hub,需配国内镜像源(阿里云专属加速器优先)或代理后重试。

---

## 七、一句话面试策略

把火力引到两层你守得住的东西:
1. **AspenTech 真实工业 B 端硬货**(性能优化、跨国协作);
2. **本项目的「我清楚每个技术选型的原因,也清楚不足与补法」**。

UL 面试官要的是「能学、诚实、懂工业领域」的人,不是完美全栈——这正好是你的最强画像。





"2024 年中我做了一个**主动的职业间歇**,主要把之前透支的健康系统调理回来——我用大半年系统学习并实践了健康管理(包括中医调理),现在身体状态很好、满血回归。这段时间我也没脱离技术,保持学习和关注行业。现在我希望进一个像 UL 这样**重视员工 well-being、有长期产品沉淀**的团队,稳定地做下去。"



"其实我特别认同 UL 把员工心理健康、体检、工作生活平衡写进福利——这和我这段经历后的想法很契合。"



团队目前的工作节奏大概怎样?有没有周期性加班?"

What is the current work pace of the team? Is there any regular overtime work? "
