-- 招聘职位表
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(100) UNIQUE NOT NULL,
    job_name VARCHAR(200) NOT NULL,
    company_name VARCHAR(200) NOT NULL,
    company_logo TEXT,
    salary_range VARCHAR(50),
    salary_min INTEGER,
    salary_max INTEGER,
    city VARCHAR(50),
    district VARCHAR(100),
    experience VARCHAR(50),
    education VARCHAR(50),
    company_scale VARCHAR(100),
    company_industry VARCHAR(100),
    finance_stage VARCHAR(50),
    job_benefits TEXT,
    posted_time VARCHAR(50),
    job_detail_url TEXT,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_jobs_job_id ON jobs(job_id);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_name);
CREATE INDEX IF NOT EXISTS idx_jobs_city ON jobs(city);
CREATE INDEX IF NOT EXISTS idx_jobs_salary_min ON jobs(salary_min);
CREATE INDEX IF NOT EXISTS idx_jobs_crawled_at ON jobs(crawled_at DESC);

-- 城市代码表
CREATE TABLE IF NOT EXISTS job_cities (
    id SERIAL PRIMARY KEY,
    city_code VARCHAR(20) UNIQUE NOT NULL,
    city_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入城市数据
INSERT INTO job_cities (city_code, city_name) VALUES
('101200300', '西安'),
('101010100', '北京'),
('101020100', '上海'),
('101280100', '广州'),
('101280600', '深圳'),
('101210100', '杭州'),
('101230200', '成都'),
('101200100', '武汉'),
('101190400', '南京')
ON CONFLICT (city_code) DO NOTHING;
