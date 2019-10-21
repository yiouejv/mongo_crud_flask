# 接口文档
    
## 添加数据: /insert/

    通过拼接url的方式传递一条记录的字段
    
    示例：
        /insert/?param1=xxx&param2=xxx
        
    返回：
        成功：成功插入！
        失败：错误提示！
        
        
## 查找数据: /find/
    
    通过拼接url的方式传递查询的条件
    示例：
        /find/?param1=xxx&param2=xxx
    返回：
        匹配的json字串
        
        
## 更新数据: /update/

    示例：
        查询param1=xxx, param2=xxx的全部记录，更新字段param1=ccc, param2=ccc
        /update/?multi=true&q_param1=xxx&q_param2=xxx&u_param1=ccc&u_param2=ccc
    参数: 
        multi
            true 
                如果查询到了多条记录, 则全部更新
            false
                查询到了多条记录,只更新第一条
        查询字段
            查询字段前加q_前缀
        更新字段     
            更新字段前加u_前缀
    返回：
        成功：影响的行数
        失败：错误提示
    

## 删除数据：/remove/
    
    示例：
        删除param1=xxx的全部记录
        /remove/?multi=true&param1=xxx
        
    参数: 
        multi
            true 
                如果查询到了多条记录, 则全部更新
            false
                查询到了多条记录,只更新第一条
        查询参数
    返回：
        成功：影响的行数
        失败：错误提示        
    
        
        
    
        

