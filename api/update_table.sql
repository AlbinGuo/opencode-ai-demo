-- 修改百度热搜表，添加图片和热搜指数字段
ALTER TABLE baidu_hot_search ADD COLUMN image_url TEXT;
ALTER TABLE baidu_hot_search ADD COLUMN hot_index TEXT;
