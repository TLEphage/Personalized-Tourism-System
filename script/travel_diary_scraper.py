import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import re
import random
from urllib.parse import urljoin, urlparse
import argparse
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TravelDiaryScraper')

# 用户代理列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1'
]

def get_random_user_agent():
    """返回随机用户代理"""
    return random.choice(USER_AGENTS)

def scrape_mafengwo_articles(url, max_pages=1, delay=1.5):
    """抓取马蜂窝旅游日记 - 更新选择器"""
    articles = []
    page = 1
    
    # 解析URL确保正确格式
    parsed_url = urlparse(url)
    if not parsed_url.path.startswith('/u/'):
        logger.error("马蜂窝URL格式不正确，应为用户主页URL: https://www.mafengwo.cn/u/用户ID/note.html")
        return articles
    
    logger.info(f"抓取马蜂窝用户: {parsed_url.path.split('/')[2]}")
    
    try:
        while page <= max_pages:
            # 构建当前页URL
            current_url = f"{url}?page={page}" if page > 1 else url
            
            headers = {
                'User-Agent': get_random_user_agent(),
                'Referer': 'https://www.mafengwo.cn/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            
            logger.info(f"抓取第 {page} 页: {current_url}")
            
            # 发送HTTP请求
            response = requests.get(current_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 检查是否被重定向
            if response.url != current_url:
                logger.warning(f"被重定向到: {response.url}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 更新选择器 - 马蜂窝2023年后的新结构
            items = soup.select('div.tn-item, div.tn-wrapper, div.notes-list > div')
            
            if not items:
                # 尝试旧版选择器
                items = soup.select('li._j_note_item, div.post-item')
                if not items:
                    logger.warning("未找到日记列表，尝试备用选择器")
                    # 尝试更通用的选择器
                    items = soup.select('div[class*="note"], div[class*="post"], li[class*="note"], li[class*="post"]')
            
            if not items:
                logger.error("无法找到日记列表，页面结构可能已更新")
                # 保存页面用于调试
                with open('mafengwo_debug.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                break
                
            logger.info(f"找到 {len(items)} 篇日记")
            
            for item in items:
                try:
                    # 提取标题
                    title_elem = item.select_one('a.tn-title, h2 > a, a.title')
                    title = title_elem.text.strip() if title_elem else "无标题"
                    
                    # 提取链接
                    link = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
                    if link and not link.startswith('http'):
                        link = urljoin('https://www.mafengwo.cn', link)
                    
                    # 提取目的地
                    place_elem = item.select_one('span.tn-place, span.tn-note, span.place')
                    place = place_elem.text.strip() if place_elem else ""
                    
                    # 提取日期
                    date_elem = item.select_one('span.tn-time, time, span.time')
                    date = date_elem.text.strip() if date_elem else "未知日期"
                    
                    # 提取统计信息
                    stats = item.select_one('div.tn-extra, div.info')
                    views = "0"
                    likes = "0"
                    if stats:
                        views_elem = stats.select_one('i.icon_view, i.view')
                        if views_elem and views_elem.next_sibling:
                            views = views_elem.next_sibling.strip()
                        
                        likes_elem = stats.select_one('i.icon_love, i.like')
                        if likes_elem and likes_elem.next_sibling:
                            likes = likes_elem.next_sibling.strip()
                    
                    # 提取摘要
                    summary_elem = item.select_one('div.tn-desc, p.txt, div.summary')
                    summary = summary_elem.text.strip() if summary_elem else ""
                    summary = re.sub(r'\s+', ' ', summary)  # 去除多余空格
                    
                    # 提取封面图片
                    img_elem = item.select_one('img')
                    image_url = ""
                    if img_elem:
                        image_url = img_elem.get('data-original') or img_elem.get('src') or ""
                    
                    article_data = {
                        'title': title,
                        'link': link,
                        'destination': place,
                        'date': date,
                        'views': views,
                        'likes': likes,
                        'summary': summary,
                        'image_url': image_url,
                        'source': '马蜂窝',
                        'page': page
                    }
                    
                    articles.append(article_data)
                    logger.info(f"  已添加: {title} - {place}")
                    
                except Exception as e:
                    logger.error(f"处理日记条目时出错: {str(e)[:100]}")
            
            # 检查是否有下一页
            next_page = soup.select_one('a.next, a.pg-next')
            if not next_page or 'disabled' in next_page.get('class', []):
                logger.info("已到达最后一页")
                break
                
            page += 1
            time.sleep(delay + random.uniform(0, 2))  # 随机延迟
            
    except requests.exceptions.RequestException as e:
        logger.error(f"请求错误: {str(e)[:100]}")
    except Exception as e:
        logger.error(f"抓取过程中出错: {str(e)[:100]}")
    
    return articles

def scrape_qyer_articles(url, max_pages=1, delay=1.5):
    """抓取穷游网旅游日记 - 更新选择器"""
    articles = []
    page = 1
    
    # 确保URL格式正确
    parsed_url = urlparse(url)
    if not parsed_url.path.startswith('/thread-'):
        logger.error("穷游网URL格式不正确，应为帖子URL: https://bbs.qyer.com/thread-帖子ID-1.html")
        return articles
    
    logger.info(f"抓取穷游网帖子: {parsed_url.path.split('/')[2]}")
    
    try:
        while page <= max_pages:
            # 构建当前页URL
            current_url = f"{url.split('.html')[0]}-{page}.html" if page > 1 else url
            
            headers = {
                'User-Agent': get_random_user_agent(),
                'Referer': 'https://bbs.qyer.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }
            
            logger.info(f"抓取第 {page} 页: {current_url}")
            
            response = requests.get(current_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # 检查是否被重定向
            if response.url != current_url:
                logger.warning(f"被重定向到: {response.url}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 更新选择器 - 穷游网新结构
            items = soup.select('div.bbs-item, div.bbs-article-item, div.bbs-thread')
            
            if not items:
                # 尝试旧版选择器
                items = soup.select('div.post-item, div.thread-item')
                if not items:
                    logger.warning("未找到日记列表，尝试备用选择器")
                    # 尝试更通用的选择器
                    items = soup.select('div[class*="item"], div[class*="thread"], div[class*="post"]')
            
            if not items:
                logger.error("无法找到日记列表，页面结构可能已更新")
                # 保存页面用于调试
                with open('qyer_debug.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                break
                
            logger.info(f"找到 {len(items)} 篇日记")
            
            for item in items:
                try:
                    # 提取标题
                    title_elem = item.select_one('a.title, h3 > a, a.subject')
                    title = title_elem.text.strip() if title_elem else "无标题"
                    
                    # 提取链接
                    link = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
                    if link and not link.startswith('http'):
                        link = urljoin('https://bbs.qyer.com', link)
                    
                    # 提取目的地
                    place_elem = item.select_one('span.place, span.destination, span.forum')
                    place = place_elem.text.strip() if place_elem else ""
                    
                    # 提取日期
                    date_elem = item.select_one('span.date, time, span.time')
                    date = date_elem.text.strip() if date_elem else "未知日期"
                    
                    # 提取统计信息
                    stats = item.select_one('div.nums, div.info, div.stats')
                    views = "0"
                    replies = "0"
                    if stats:
                        views_elem = stats.select_one('em.views, em.read')
                        if views_elem:
                            views = views_elem.text.strip()
                        
                        replies_elem = stats.select_one('em.replies, em.comments')
                        if replies_elem:
                            replies = replies_elem.text.strip()
                    
                    # 提取摘要
                    summary_elem = item.select_one('p.text, div.summary, div.content')
                    summary = summary_elem.text.strip() if summary_elem else ""
                    summary = re.sub(r'\s+', ' ', summary)  # 去除多余空格
                    
                    # 提取封面图片
                    img_elem = item.select_one('img')
                    image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                    
                    article_data = {
                        'title': title,
                        'link': link,
                        'destination': place,
                        'date': date,
                        'views': views,
                        'replies': replies,
                        'summary': summary,
                        'image_url': image_url,
                        'source': '穷游网',
                        'page': page
                    }
                    
                    articles.append(article_data)
                    logger.info(f"  已添加: {title} - {place}")
                    
                except Exception as e:
                    logger.error(f"处理日记条目时出错: {str(e)[:100]}")
            
            # 检查是否有下一页
            next_page = soup.select_one('a.next, a.page-next')
            if not next_page or 'disabled' in next_page.get('class', []):
                logger.info("已到达最后一页")
                break
                
            page += 1
            time.sleep(delay + random.uniform(0, 2))  # 随机延迟
            
    except requests.exceptions.RequestException as e:
        logger.error(f"请求错误: {str(e)[:100]}")
    except Exception as e:
        logger.error(f"抓取过程中出错: {str(e)[:100]}")
    
    return articles

def scrape_ctrip_articles(url, max_pages=1, delay=1.5):
    """抓取携程游记 - 更新URL结构和选择器"""
    articles = []
    page = 1
    
    # 确保URL格式正确
    parsed_url = urlparse(url)
    if not parsed_url.path.startswith('/travels/'):
        logger.error("携程URL格式不正确，应为目的地游记URL: https://you.ctrip.com/travels/目的地/")
        return articles
    
    # 提取目的地
    destination = parsed_url.path.split('/')[2]
    logger.info(f"抓取携程目的地: {destination}")
    
    try:
        while page <= max_pages:
            # 构建当前页URL - 携程的特殊分页结构
            if page == 1:
                current_url = f"https://you.ctrip.com/travels/{destination}/"
            else:
                current_url = f"https://you.ctrip.com/travels/{destination}/t3-p{page}.html"
            
            headers = {
                'User-Agent': get_random_user_agent(),
                'Referer': 'https://you.ctrip.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
            
            logger.info(f"抓取第 {page} 页: {current_url}")
            
            response = requests.get(current_url, headers=headers, timeout=15)
            
            # 检查状态码
            if response.status_code == 404:
                logger.warning(f"页面不存在: {current_url}")
                break
                
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 更新选择器 - 携程新结构
            items = soup.select('div.journey-item, div.travels_list')
            
            if not items:
                # 尝试旧版选择器
                items = soup.select('div.list_item, div.travels_item')
                if not items:
                    logger.warning("未找到日记列表，尝试备用选择器")
                    # 尝试更通用的选择器
                    items = soup.select('div[class*="item"], div[class*="travel"], div[class*="journey"]')
            
            if not items:
                logger.error("无法找到日记列表，页面结构可能已更新")
                # 保存页面用于调试
                with open('ctrip_debug.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                break
                
            logger.info(f"找到 {len(items)} 篇日记")
            
            for item in items:
                try:
                    # 提取标题
                    title_elem = item.select_one('a.title, h2 > a, a.name')
                    title = title_elem.text.strip() if title_elem else "无标题"
                    
                    # 提取链接
                    link = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""
                    if link and not link.startswith('http'):
                        link = urljoin('https://you.ctrip.com', link)
                    
                    # 提取目的地
                    place_elem = item.select_one('span.ellipsis, span.destination, span.place')
                    place = place_elem.text.strip() if place_elem else destination
                    
                    # 提取日期
                    date_elem = item.select_one('span.time, time, span.date')
                    date = date_elem.text.strip() if date_elem else "未知日期"
                    
                    # 提取统计信息
                    stats = item.select_one('div.counts, div.info, div.stats')
                    views = "0"
                    comments = "0"
                    if stats:
                        views_elem = stats.select_one('i.numview, em.view')
                        if views_elem:
                            views = views_elem.text.strip()
                        
                        comments_elem = stats.select_one('i.numreply, em.reply')
                        if comments_elem:
                            comments = comments_elem.text.strip()
                    
                    # 提取摘要
                    summary_elem = item.select_one('p.journey-desc, div.summary, div.content')
                    summary = summary_elem.text.strip() if summary_elem else ""
                    summary = re.sub(r'\s+', ' ', summary)  # 去除多余空格
                    
                    # 提取封面图片
                    img_elem = item.select_one('img')
                    image_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                    
                    article_data = {
                        'title': title,
                        'link': link,
                        'destination': place,
                        'date': date,
                        'views': views,
                        'comments': comments,
                        'summary': summary,
                        'image_url': image_url,
                        'source': '携程',
                        'page': page
                    }
                    
                    articles.append(article_data)
                    logger.info(f"  已添加: {title} - {place}")
                    
                except Exception as e:
                    logger.error(f"处理日记条目时出错: {str(e)[:100]}")
            
            # 检查是否有下一页
            next_page = soup.select_one('a.nextpage, a.next')
            if not next_page or 'disabled' in next_page.get('class', []):
                logger.info("已到达最后一页")
                break
                
            page += 1
            time.sleep(delay + random.uniform(0, 2))  # 随机延迟
            
    except requests.exceptions.RequestException as e:
        logger.error(f"请求错误: {str(e)[:100]}")
    except Exception as e:
        logger.error(f"抓取过程中出错: {str(e)[:100]}")
    
    return articles

def detect_platform(url):
    """根据URL检测平台"""
    if 'mafengwo' in url:
        return 'mafengwo'
    elif 'qyer' in url:
        return 'qyer'
    elif 'ctrip' in url or 'trip.com' in url:
        return 'ctrip'
    else:
        return 'unknown'

def scrape_travel_diaries(url, max_pages=1, delay=1.5):
    """根据URL自动选择平台抓取旅游日记"""
    platform = detect_platform(url)
    logger.info(f"检测到平台: {platform}")
    
    if platform == 'mafengwo':
        return scrape_mafengwo_articles(url, max_pages, delay)
    elif platform == 'qyer':
        return scrape_qyer_articles(url, max_pages, delay)
    elif platform == 'ctrip':
        return scrape_ctrip_articles(url, max_pages, delay)
    else:
        logger.error(f"不支持的平台: {url}")
        return []

def save_to_csv(articles, output_file):
    """将结果保存为CSV文件"""
    if not articles:
        logger.warning("没有数据可保存")
        return False
    
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # 动态确定字段名
            fieldnames = set()
            for article in articles:
                fieldnames.update(article.keys())
            
            writer = csv.DictWriter(csvfile, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(articles)
        
        logger.info(f"成功保存 {len(articles)} 篇日记到: {os.path.abspath(output_file)}")
        return True
    except Exception as e:
        logger.error(f"保存CSV文件时出错: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='旅游日记批量抓取工具')
    parser.add_argument('url', help='博主主页或日记列表URL')
    parser.add_argument('-p', '--pages', type=int, default=1, help='最大抓取页数 (默认: 1)')
    parser.add_argument('-d', '--delay', type=float, default=2.0, help='请求延迟时间(秒) (默认: 2.0)')
    parser.add_argument('-o', '--output', default='travel_diaries.csv', help='输出文件名 (默认: travel_diaries.csv)')
    
    args = parser.parse_args()
    
    logger.info(f"开始抓取旅游日记: {args.url}")
    logger.info(f"最大页数: {args.pages}, 延迟: {args.delay}秒")
    
    # 执行抓取
    articles = scrape_travel_diaries(
        url=args.url,
        max_pages=args.pages,
        delay=args.delay
    )
    
    # 保存结果
    if articles:
        save_to_csv(articles, args.output)
        
        # 显示前5篇日记摘要
        logger.info("\n抓取结果预览 (前5篇):")
        for i, article in enumerate(articles[:5]):
            print(f"【{article.get('source', '未知平台')}】{article.get('title', '无标题')}")
            print(f"目的地: {article.get('destination', '未知')}")
            print(f"日期: {article.get('date', '未知')}")
            print(f"摘要: {article.get('summary', '无摘要')[:100]}...")
            print(f"链接: {article.get('link', '')}")
            
            # 根据平台显示不同的统计信息
            stats = []
            if 'views' in article:
                stats.append(f"浏览: {article['views']}")
            if 'likes' in article:
                stats.append(f"点赞: {article['likes']}")
            if 'replies' in article:
                stats.append(f"回复: {article['replies']}")
            if 'comments' in article:
                stats.append(f"评论: {article['comments']}")
                
            print(f"统计: {' '.join(stats)}")
            print("-" * 80)
    else:
        logger.warning("未获取到任何日记数据")

if __name__ == "__main__":
    main()