"""
Boss直聘招聘数据采集模块
用于获取外企招聘信息，并存储到数据库
"""
import requests
import json
import random
import time
import psycopg2
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel
from db_config import get_connection_params


class JobBase(BaseModel):
    """招聘职位基础信息"""
    job_id: str
    job_name: str
    company_name: str
    company_logo: str = ""
    salary_range: str = ""
    salary_min: int = 0
    salary_max: int = 0
    city: str = ""
    district: str = ""
    experience: str = ""
    education: str = ""
    company_scale: str = ""
    company_industry: str = ""
    finance_stage: str = ""
    job_benefits: List[str] = []
    posted_time: str = ""
    job_detail_url: str = ""


JobInfo = JobBase


class JobsDB:
    """招聘数据数据库操作类"""

    def __init__(self):
        self.conn = None

    def get_connection(self):
        """获取数据库连接"""
        try:
            return psycopg2.connect(**get_connection_params())
        except Exception as e:
            print(f"数据库连接错误: {e}")
            return None
    
    def save_job(self, job: Dict) -> bool:
        """保存或更新职位信息"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cur = conn.cursor()
            benefits_json = json.dumps(job.get("job_benefits", []), ensure_ascii=False)
            
            cur.execute("""
                INSERT INTO jobs (
                    job_id, job_name, company_name, company_logo,
                    salary_range, salary_min, salary_max,
                    city, district, experience, education,
                    company_scale, company_industry, finance_stage,
                    job_benefits, posted_time, job_detail_url,
                    updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
                ON CONFLICT (job_id) DO UPDATE SET
                    job_name = EXCLUDED.job_name,
                    company_name = EXCLUDED.company_name,
                    company_logo = EXCLUDED.company_logo,
                    salary_range = EXCLUDED.salary_range,
                    salary_min = EXCLUDED.salary_min,
                    salary_max = EXCLUDED.salary_max,
                    city = EXCLUDED.city,
                    district = EXCLUDED.district,
                    experience = EXCLUDED.experience,
                    education = EXCLUDED.education,
                    company_scale = EXCLUDED.company_scale,
                    company_industry = EXCLUDED.company_industry,
                    finance_stage = EXCLUDED.finance_stage,
                    job_benefits = EXCLUDED.job_benefits,
                    posted_time = EXCLUDED.posted_time,
                    job_detail_url = EXCLUDED.job_detail_url,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                job.get("job_id"),
                job.get("job_name"),
                job.get("company_name"),
                job.get("company_logo", ""),
                job.get("salary_range", ""),
                job.get("salary_min", 0),
                job.get("salary_max", 0),
                job.get("city", ""),
                job.get("district", ""),
                job.get("experience", ""),
                job.get("education", ""),
                job.get("company_scale", ""),
                job.get("company_industry", ""),
                job.get("finance_stage", ""),
                benefits_json,
                job.get("posted_time", ""),
                job.get("job_detail_url", "")
            ))
            
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"保存职位失败: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def save_jobs_batch(self, jobs: List[Dict]) -> int:
        """批量保存职位信息"""
        saved_count = 0
        for job in jobs:
            if self.save_job(job):
                saved_count += 1
        return saved_count
    
    def get_jobs(
        self,
        city: str = None,
        query: str = None,
        page: int = 1,
        page_size: int = 10,
        finance_stage: str = None,
        min_salary: int = None,
        max_salary: int = None
    ) -> Dict:
        """从数据库获取职位列表"""
        conn = self.get_connection()
        if not conn:
            return {"data": [], "total": 0}
        
        try:
            cur = conn.cursor()
            
            # 构建查询条件
            conditions = []
            params = []
            
            if city:
                conditions.append("city = %s")
                params.append(city)
            
            if query:
                conditions.append("(job_name ILIKE %s OR company_name ILIKE %s)")
                params.extend([f"%{query}%", f"%{query}%"])
            
            if finance_stage:
                conditions.append("finance_stage = %s")
                params.append(finance_stage)
            
            if min_salary:
                conditions.append("salary_min >= %s")
                params.append(min_salary)
            
            if max_salary:
                conditions.append("salary_max <= %s")
                params.append(max_salary)
            
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            
            # 查询总数
            count_sql = f"SELECT COUNT(*) FROM jobs WHERE {where_clause}"
            cur.execute(count_sql, params)
            total = cur.fetchone()[0]
            
            # 查询数据
            offset = (page - 1) * page_size
            sql = f"""
                SELECT id, job_id, job_name, company_name, company_logo,
                       salary_range, salary_min, salary_max,
                       city, district, experience, education,
                       company_scale, company_industry, finance_stage,
                       job_benefits, posted_time, job_detail_url
                FROM jobs
                WHERE {where_clause}
                ORDER BY id DESC
                LIMIT %s OFFSET %s
            """
            params.extend([page_size, offset])
            cur.execute(sql, params)
            
            results = cur.fetchall()
            cur.close()
            conn.close()
            
            jobs = []
            for row in results:
                benefits = []
                if row[14]:
                    try:
                        benefits = json.loads(row[14])
                    except:
                        pass
                
                jobs.append({
                    "id": row[0],
                    "job_id": row[1],
                    "job_name": row[2],
                    "company_name": row[3],
                    "company_logo": row[4] or "",
                    "salary_range": row[5] or "",
                    "salary_min": row[6] or 0,
                    "salary_max": row[7] or 0,
                    "city": row[8] or "",
                    "district": row[9] or "",
                    "experience": row[10] or "",
                    "education": row[11] or "",
                    "company_scale": row[12] or "",
                    "company_industry": row[13] or "",
                    "finance_stage": row[14] or "",
                    "job_benefits": benefits,
                    "posted_time": row[16] or "",
                    "detail_url": row[17] or ""
                })
            
            return {
                "data": jobs,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        except Exception as e:
            print(f"查询职位失败: {e}")
            return {"data": [], "total": 0}
    
    def get_jobs_count(self) -> int:
        """获取数据库中的职位总数"""
        conn = self.get_connection()
        if not conn:
            return 0
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM jobs")
            count = cur.fetchone()[0]
            cur.close()
            conn.close()
            return count
        except Exception as e:
            print(f"获取职位数量失败: {e}")
            return 0
    
    def get_job_by_id(self, job_id: int) -> Optional[Dict]:
        """根据ID获取单个职位详情"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT job_id, job_name, company_name, company_logo,
                       salary_range, salary_min, salary_max,
                       city, district, experience, education,
                       company_scale, company_industry, finance_stage,
                       job_benefits, posted_time, job_detail_url
                FROM jobs
                WHERE id = %s
            """, (job_id,))
            
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if not row:
                return None
            
            benefits = []
            if row[14]:
                try:
                    benefits = json.loads(row[14])
                except:
                    pass
            
            return {
                "id": job_id,
                "job_id": row[0],
                "job_name": row[1],
                "company_name": row[2],
                "company_logo": row[3] or "",
                "salary_range": row[4] or "",
                "salary_min": row[5] or 0,
                "salary_max": row[6] or 0,
                "city": row[7] or "",
                "district": row[8] or "",
                "experience": row[9] or "",
                "education": row[10] or "",
                "company_scale": row[11] or "",
                "company_industry": row[12] or "",
                "finance_stage": row[13] or "",
                "job_benefits": benefits,
                "posted_time": row[15] or "",
                "detail_url": row[16] or ""
            }
        except Exception as e:
            print(f"查询职位详情失败: {e}")
            return None
    
    def clear_old_jobs(self, days: int = 30) -> int:
        """清理旧数据"""
        conn = self.get_connection()
        if not conn:
            return 0
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM jobs WHERE crawled_at < NOW() - INTERVAL '%s days'", (days,))
            deleted = cur.rowcount
            conn.commit()
            cur.close()
            conn.close()
            return deleted
        except Exception as e:
            print(f"清理旧数据失败: {e}")
            return 0


class BossZhipinSpider:
    """Boss直聘爬虫"""
    
    def __init__(self, cookie: str = None):
        self.base_url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
        self.detail_url = "https://www.zhipin.com/wapi/zpgeek/job/detail.json"
        self.session = requests.Session()
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://www.zhipin.com/",
            "Origin": "https://www.zhipin.com"
        }
        
        if cookie:
            self.headers["Cookie"] = cookie
        
        self.session.headers.update(self.headers)
    
    def get_jobs(
        self,
        query: str = "Python",
        city: str = "101010100",
        page: int = 1,
        page_size: int = 30,
        experience: str = None,
        education: str = None,
        scale: str = None,
        finance: str = None,
        industry: str = None
    ) -> List[Dict]:
        """
        获取职位列表
        
        Args:
            query: 搜索关键词
            city: 城市代码 (101010100=北京, 101020100=上海, 101280100=广州, 101280600=深圳)
            page: 页码
            page_size: 每页数量
            experience: 经验要求 (106=应届生, 101=1年以下, 102=1-3年, 103=3-5年, 104=5-10年, 105=10年以上)
            education: 学历要求 (207=中专及以下, 206=高中, 205=大专, 204=本科, 203=硕士, 202=博士)
            scale: 公司规模 (303=20人以下, 304=20-99人, 305=100-499人, 306=500-999人, 307=1000-9999人, 308=10000人以上)
            finance: 融资阶段 (startup_early=初创型, startup=成长型, listed=上市公司)
            industry: 行业
        """
        params = {
            "query": query,
            "city": city,
            "page": page,
            "pageSize": page_size
        }
        
        if experience:
            params["experience"] = experience
        if education:
            params["education"] = education
        if scale:
            params["scale"] = scale
        if finance:
            params["finance"] = finance
        if industry:
            params["industry"] = industry
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("code") == 0:
                return data.get("zpData", {}).get("jobList", [])
            else:
                print(f"API返回错误: {data.get('message')}")
                return []
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return []
    
    def parse_job(self, job_data: Dict) -> Optional[JobInfo]:
        """解析职位数据"""
        try:
            salary = job_data.get("salary", "")
            salary_range = salary.replace("K", "k").replace("k", "K")
            
            salary_parts = salary.replace("K", "").replace("k", "").split("-")
            salary_min = int(salary_parts[0]) * 1000 if len(salary_parts) >= 1 else 0
            salary_max = int(salary_parts[1]) * 1000 if len(salary_parts) >= 2 else salary_min
            
            location = job_data.get("location", {})
            cityDistrict = job_data.get("cityDistrict", {})
            
            job = JobInfo(
                job_id=job_data.get("encryptJobId", ""),
                job_name=job_data.get("jobName", ""),
                company_name=job_data.get("brandName", ""),
                company_logo=job_data.get("brandLogo", ""),
                salary_range=salary_range,
                salary_min=salary_min,
                salary_max=salary_max,
                city=location.get("name", ""),
                district=cityDistrict.get("name", ""),
                experience=job_data.get("experience", ""),
                education=job_data.get("education", ""),
                company_scale=job_data.get("scaleName", ""),
                company_industry=job_data.get("industryName", ""),
                finance_stage=job_data.get("financeName", ""),
                job_benefits=job_data.get("jobBenefits", []),
                posted_time=job_data.get("publicedTime", ""),
                job_detail_url=f"https://www.zhipin.com/job_detail/{job_data.get('encryptJobId', '')}.html"
            )
            
            return job
        except Exception as e:
            print(f"解析职位数据失败: {e}")
            return None
    
    def get_foreign_jobs(
        self,
        query: str = "Python",
        city: str = "101010100",
        page: int = 1,
        max_pages: int = 3
    ) -> List[JobInfo]:
        """
        获取外企招聘信息
        外企特征：外资/已上市，规模较大，福利好
        """
        jobs = []
        
        scale_options = ["305", "306", "307", "308"]
        finance_options = ["listed"]
        
        for p in range(page, min(page + max_pages, 10)):
            print(f"正在采集第 {p} 页...")
            
            page_jobs = self.get_jobs(
                query=query,
                city=city,
                page=p,
                page_size=30,
                scale=",".join(scale_options),
                finance=",".join(finance_options)
            )
            
            for job_data in page_jobs:
                job = self.parse_job(job_data)
                if job:
                    jobs.append(job)
            
            time.sleep(random.uniform(1, 3))
        
        return jobs
    
    def get_job_detail(self, job_id: str) -> Optional[Dict]:
        """获取职位详情"""
        try:
            response = self.session.get(
                self.detail_url,
                params={"encryptJobId": job_id},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get("code") == 0:
                return data.get("zpData", {})
            return None
        except Exception as e:
            print(f"获取职位详情失败: {e}")
            return None


def get_foreign_jobs_sample() -> List[Dict]:
    """
    模拟外企招聘数据（用于开发测试）
    实际使用需要配置真实的Cookie
    """
    sample_jobs = [
        {
            "job_id": "1",
            "job_name": "Python高级开发工程师",
            "company_name": "Microsoft",
            "company_logo": "",
            "salary_range": "30K-50K",
            "salary_min": 30000,
            "salary_max": 50000,
            "city": "北京",
            "district": "朝阳区",
            "experience": "3-5年",
            "education": "本科",
            "company_scale": "1000-9999人",
            "company_industry": "互联网",
            "finance_stage": "上市公司",
            "job_benefits": ["五险一金", "带薪年假", "年度体检", "股票期权"],
            "posted_time": "今天发布",
            "job_detail_url": "https://www.zhipin.com/job_detail/1.html"
        },
        {
            "job_id": "2",
            "job_name": "数据工程师",
            "company_name": "Amazon",
            "company_logo": "",
            "salary_range": "25K-40K",
            "salary_min": 25000,
            "salary_max": 40000,
            "city": "北京",
            "district": "海淀区",
            "experience": "2-5年",
            "education": "本科",
            "company_scale": "10000人以上",
            "company_industry": "互联网",
            "finance_stage": "上市公司",
            "job_benefits": ["六险一金", "弹性工作", "技术培训"],
            "posted_time": "2天前发布",
            "job_detail_url": "https://www.zhipin.com/job_detail/2.html"
        },
        {
            "job_id": "3",
            "job_name": "后端开发工程师",
            "company_name": "Google",
            "company_logo": "",
            "salary_range": "35K-60K",
            "salary_min": 35000,
            "salary_max": 60000,
            "city": "上海",
            "district": "浦东新区",
            "experience": "3-5年",
            "education": "本科",
            "company_scale": "10000人以上",
            "company_industry": "互联网",
            "finance_stage": "上市公司",
            "job_benefits": ["免费三餐", "健身房", "股票期权"],
            "posted_time": "今天发布",
            "job_detail_url": "https://www.zhipin.com/job_detail/3.html"
        },
        {
            "job_id": "4",
            "job_name": "全栈开发工程师",
            "company_name": "Apple",
            "company_logo": "",
            "salary_range": "28K-45K",
            "salary_min": 28000,
            "salary_max": 45000,
            "city": "深圳",
            "district": "南山区",
            "experience": "2-4年",
            "education": "本科",
            "company_scale": "1000-9999人",
            "company_industry": "互联网",
            "finance_stage": "上市公司",
            "job_benefits": ["五险一金", "年终奖金", "员工旅游"],
            "posted_time": "3天前发布",
            "job_detail_url": "https://www.zhipin.com/job_detail/4.html"
        },
        {
            "job_id": "5",
            "job_name": "机器学习工程师",
            "company_name": "Meta",
            "company_logo": "",
            "salary_range": "40K-70K",
            "salary_min": 40000,
            "salary_max": 70000,
            "city": "北京",
            "district": "中关村",
            "experience": "3-5年",
            "education": "硕士",
            "company_scale": "1000-9999人",
            "company_industry": "人工智能",
            "finance_stage": "上市公司",
            "job_benefits": ["高额奖金", "技术挑战", "国际化团队"],
            "posted_time": "今天发布",
            "job_detail_url": "https://www.zhipin.com/job_detail/5.html"
        }
    ]
    
    return sample_jobs


def crawl_and_save_jobs(query: str = "Python", city: str = "101200300", max_pages: int = 3) -> Dict:
    """
    爬取招聘数据并保存到数据库
    
    Args:
        query: 搜索关键词
        city: 城市代码
        max_pages: 最大爬取页数
    
    Returns:
        包含爬取结果的字典
    """
    spider = BossZhipinSpider()
    db = JobsDB()
    
    print(f"开始爬取 {query} 相关职位数据，城市代码: {city}")
    
    all_jobs = []
    saved_count = 0
    
    for page in range(1, max_pages + 1):
        print(f"正在爬取第 {page} 页...")
        
        try:
            page_jobs = spider.get_jobs(
                query=query,
                city=city,
                page=page,
                page_size=30,
                scale="305,306,307,308",
                finance="listed"
            )
            
            if not page_jobs:
                print(f"第 {page} 页无数据，停止爬取")
                break
            
            for job_data in page_jobs:
                job = spider.parse_job(job_data)
                if job:
                    job_dict = {
                        "job_id": job.job_id,
                        "job_name": job.job_name,
                        "company_name": job.company_name,
                        "company_logo": job.company_logo,
                        "salary_range": job.salary_range,
                        "salary_min": job.salary_min,
                        "salary_max": job.salary_max,
                        "city": job.city,
                        "district": job.district,
                        "experience": job.experience,
                        "education": job.education,
                        "company_scale": job.company_scale,
                        "company_industry": job.company_industry,
                        "finance_stage": job.finance_stage,
                        "job_benefits": job.job_benefits,
                        "posted_time": job.posted_time,
                        "job_detail_url": job.job_detail_url
                    }
                    all_jobs.append(job_dict)
            
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"爬取第 {page} 页失败: {e}")
            continue
    
    if all_jobs:
        saved_count = db.save_jobs_batch(all_jobs)
    
    return {
        "crawled": len(all_jobs),
        "saved": saved_count,
        "query": query,
        "city": city
    }


def get_jobs_from_db(
    query: str = None,
    city: str = None,
    page: int = 1,
    page_size: int = 10
) -> Dict:
    """
    从数据库获取职位列表
    
    Args:
        query: 搜索关键词
        city: 城市代码
        page: 页码
        page_size: 每页数量
    
    Returns:
        包含职位列表的字典
    """
    db = JobsDB()
    return db.get_jobs(
        query=query,
        city=city,
        page=page,
        page_size=page_size
    )


if __name__ == "__main__":
    spider = BossZhipinSpider()
    
    print("开始采集外企招聘信息...")
    jobs = spider.get_foreign_jobs(query="Python", city="101010100", page=1, max_pages=1)
    
    for i, job in enumerate(jobs[:5], 1):
        print(f"\n[{i}] {job.job_name}")
        print(f"    公司: {job.company_name}")
        print(f"    薪资: {job.salary_range}")
        print(f"    地点: {job.city} {job.district}")
        print(f"    规模: {job.company_scale}")
        print(f"    福利: {', '.join(job.job_benefits[:3])}")
