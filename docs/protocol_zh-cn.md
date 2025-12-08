# 智能体狼人杀通信协议

## 1. 协议概述

本协议定义了狼人杀游戏服务器（后端）与AI智能体SDK之间的通信接口。协议采用函数调用模式，后端在游戏特定阶段调用SDK中的特定函数，智能体返回决策结果。

## 2. 基础约定

- **通信方式**: JSON-RPC 2.0风格
    
- **编码**: UTF-8
    
- **时间限制**: 每个调用必须在指定时间内响应（通常5-10秒）
    
- **错误处理**: 超时或错误将视为弃权或默认行为
    

## 3. 核心数据结构

```typescript
// 通用数据结构
interface Player {
  player_id: number;      // 玩家唯一ID
  name: string;          // 玩家名称
  is_alive: boolean;     // 是否存活
  role?: string;         // 角色（仅在知晓时提供）
}

interface GameState {
  day_number: number;    // 当前天数（第几天）
  phase: string;         // 当前阶段
  alive_players: Player[]; // 存活玩家列表
  dead_players: Player[];  // 死亡玩家列表
  history: GameEvent[];  // 历史事件
}

interface GameEvent {
  event_type: string;    // 事件类型
  day: number;           // 发生天数
  phase: string;         // 发生阶段
  data: any;             // 事件数据
}
```
## 4. 函数调用规范

### 4.1. 初始化函数

#### `initialize`

**调用时机**: 游戏开始前，仅调用一次

**传入数据**:
```json
{
  "player_id": 123,
  "role": "werewolf",
  "role_description": "你是狼人，每晚可以杀死一名玩家...",
  "all_players": [
    {"player_id": 123, "name": "玩家A"},
    {"player_id": 124, "name": "玩家B"}
  ],
  "game_config": {
    "roles": ["werewolf", "seer", "witch", "villager"],
    "wolf_count": 2,
    "max_days": 10,
    "language": "zh-CN"
  }
}
```

**返回值**:
```json
{
  "status": "success",
  "message": "初始化完成"
}
```
### 4.2. 夜晚阶段函数

#### `werewolf_action` (狼人行动)

**调用时机**: 夜晚阶段，仅对狼人角色调用

**传入数据**:
```json
{
  "game_state": GameState,
  "night_number": 1,
  "alive_players": Player[],          // 所有存活玩家
  "teammates": Player[],              // 狼队友（仅存活狼人）
  "previous_votes": [                 // 历史狼人投票（如有）
    {
      "night": 0,
      "target_id": 124,
      "voted_by": [123, 125]
    }
  ]
}
```

**返回值**:
```json
{
  "action": "kill",
  "target_id": 124,                  // 要击杀的玩家ID
  "reasoning": "我怀疑他是预言家...",   // 决策理由（可选）
  "confidence": 0.85                  // 置信度（0-1）
}
```

#### `seer_action` (预言家行动)

**调用时机**: 夜晚阶段，仅对预言家角色调用

**传入数据**:
```json
{
  "game_state": GameState,
  "night_number": 1,
  "alive_players": Player[],          // 所有存活玩家
  "previous_checks": [                // 历史查验结果
    {
      "night": 0,
      "target_id": 124,
      "role": "villager"
    }
  ]
}
```

**返回值**:
```json
{
  "action": "check",
  "target_id": 125,                   // 要查验的玩家ID
  "reasoning": "他发言有疑点..."      // 决策理由（可选）
}
```
#### `witch_action` (女巫行动)

**调用时机**: 夜晚阶段，仅对女巫角色调用

**传入数据**:
```json
{
  "game_state": GameState,
  "night_number": 1,
  "alive_players": Player[],          // 所有存活玩家
  "poison_available": true,           // 毒药是否可用
  "antidote_available": true,         // 解药是否可用
  "killed_player_id": 124,            // 今晚被狼杀的目标（可为null）
  "previous_actions": [               // 历史行动
    {
      "night": 0,
      "action": "save",
      "target_id": 123
    }
  ]
}
```

**返回值**:
```json
{
  "action": "save",                   // "save", "poison", "abstain"
  "target_id": 124,                   // 使用解药/毒药的目标（如适用）
  "reasoning": "我认为他可能是好人..." // 决策理由
}
```
#### `hunter_action` (猎人行动，被触发时)

**调用时机**: 猎人被放逐或杀死时立即调用

**传入数据**:
```json
{
  "game_state": GameState,
  "cause": "vote",                    // "vote"被投票或"kill"被杀死
  "killed_by": 125,                   // 导致死亡的玩家ID（如可追踪）
  "alive_players": Player[]           // 所有存活玩家
}
```

**返回值**:
```json
{
  "action": "shoot",                  // "shoot"或"abstain"
  "target_id": 126,                   // 要射击的玩家ID
  "reasoning": "他是最后一匹狼..."      // 决策理由
}
```
### 4.3. 白天阶段函数

#### `discuss` (讨论发言)

**调用时机**: 白天讨论阶段，每轮可能多次调用

**传入数据**:
```json
{
  "game_state": GameState,
  "day_number": 1,
  "speech_order": 3,                  // 发言顺序
  "previous_speeches": [              // 之前玩家的发言
    {
      "player_id": 123,
      "content": "我认为2号玩家可疑...",
      "round": 1
    }
  ],
  "last_night_events": GameEvent[],   // 昨晚发生的事件（公开信息）
  "remaining_time": 60                // 剩余发言时间（秒）
}
```

**返回值**:
```json
{
  "speech": "我同意1号的观点，但3号玩家昨晚的行为...",
  "emotion": "neutral",               // "neutral", "suspicious", "confident"等
  "target_players": [124, 125],       // 提及的玩家ID
  "is_accusation": false              // 是否为指控性发言
}
```

#### `vote` (投票)

**调用时机**: 白天投票阶段

**传入数据**:
```json
{
  "game_state": GameState,
  "day_number": 1,
  "alive_players": Player[],          // 所有存活玩家
  "discussion_summary": "玩家A指控玩家B...", // 讨论摘要
  "previous_votes": [                 // 历史投票记录
    {
      "day": 0,
      "votes": {"123": 2, "124": 3}
    }
  ],
  "vote_type": "elimination"          // "elimination"或"pk"
}
```

**返回值**:
```json
{
  "vote_target": 124,                 // 投票目标ID，null表示弃权
  "reasoning": "他的发言有明显矛盾...", // 投票理由
  "confidence": 0.75                   // 置信度
}
```

### 4.4. 特殊状态函数

#### `defend` (辩护)

**调用时机**: 当玩家被指控或处于PK环节时

**传入数据**:
```json
{
  "game_state": GameState,
  "accusations": [                    // 受到的指控
    {
      "accuser_id": 123,
      "content": "你昨晚行为可疑...",
      "evidence": ["speech_round_2"]
    }
  ],
  "time_limit": 30                    // 辩护时间限制
}
```

**返回值**:
```json
{
  "defense": "我昨晚是因为...",
  "counter_arguments": [              // 反驳点
    {
      "against_player": 123,
      "point": "你昨天也投了错误的人"
    }
  ],
  "emotional_tone": "calm"            // 情绪基调
}
```
### 4.5. 游戏结束函数

#### `game_over`

**调用时机**: 游戏结束时

**传入数据**:
```json
{
  "winner": "werewolves",             // 获胜方
  "winning_players": [123, 125],      // 获胜玩家
  "final_state": GameState,
  "role_reveal": [                    // 角色揭示
    {"player_id": 123, "role": "werewolf"},
    {"player_id": 124, "role": "seer"}
  ],
  "performance_stats": {              // 表现统计
    "accuracy": 0.8,
    "contribution": 0.7
  }
}
```

**返回值**:
```json
{
  "status": "acknowledged",
  "reflection": "我作为狼人应该更早刀掉预言家...", // 反思总结
  "rating": 4.5                       // 自评分数（1-5）
}
```
## 5. 错误处理

### 5.1. 超时处理

- 函数调用超过时限未响应，将使用默认行为
    
- 狼人/预言家超时：视为放弃行动
    
- 女巫超时：视为不使用药剂
    
- 投票超时：视为弃权
    

### 5.2. 错误响应格式

```json
{
  "error": {
    "code": 1001,
    "message": "Invalid target player",
    "suggested_action": "abstain"
  }
}
```

### 5.3. 错误码表

|代码|说明|建议行动|
|---|---|---|
|1001|无效的目标玩家|放弃行动|
|1002|无效的行动类型|使用默认|
|1003|内部逻辑错误|随机选择|
|1004|数据格式错误|放弃行动|

## 6. 游戏流程示例

```text

游戏开始
  后端调用所有智能体: initialize()
  
第1夜
  后端调用狼人: werewolf_action()
  后端调用预言家: seer_action()
  后端调用女巫: witch_action()
  
第1天
  循环发言:
    后端调用当前发言玩家: discuss()
  后端调用所有存活玩家: vote()
  
  如有PK:
    后端调用PK玩家: defend()
    后端调用所有玩家: vote()  // PK投票
    
游戏继续或结束:
  如游戏继续，重复夜晚-白天循环
  游戏结束:
    后端调用所有玩家: game_over()
```

## 7. 扩展性说明

1. **角色扩展**: 新增角色时，添加对应的action函数
    
2. **功能扩展**: 新增游戏机制时，可添加新的函数或扩展现有函数参数
    
3. **多语言**: 通过game_config中的language字段支持多语言
    
4. **观察者模式**: 可添加observer_update函数供观战AI使用
    

## 8. 实现要求

1. SDK必须实现所有相关角色的函数
	
2. 函数必须是幂等的（相同输入产生相同输出）
    
3. 必须处理所有可能的输入状态
    
4. 建议添加本地日志记录功能
    

---

_本协议为智能体狼人杀游戏的标准通信协议，第三方SDK开发者应严格遵循此协议实现相应接口。_