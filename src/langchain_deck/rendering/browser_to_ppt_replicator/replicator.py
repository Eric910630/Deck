"""
浏览器到PPT复刻器 - 主入口
整合所有模块，实现完整的复刻流程
"""

from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger

from .browser_renderer import BrowserRenderer
from .element_analyzer import ElementAnalyzer
from .coordinate_mapper import CoordinateMapper
from .container_extractor import ContainerExtractor
from .text_extractor import TextExtractor
from .ppt_replicator import PPTReplicator


class BrowserToPPTReplicator:
    """
    浏览器到PPT复刻器
    将浏览器渲染的Ant Design/AntV组件一比一复刻到PPT
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化复刻器
        
        Args:
            output_dir: 输出目录（容器图片和PPT文件）
        """
        if output_dir is None:
            output_dir = Path.cwd() / "replicated_outputs"
        else:
            output_dir = Path(output_dir)
        
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        self.containers_dir = self.output_dir / "containers"
        self.containers_dir.mkdir(exist_ok=True)
        
        # 初始化组件
        self.coordinate_mapper = CoordinateMapper()
        self.element_analyzer = ElementAnalyzer()
        self.container_extractor = ContainerExtractor(self.containers_dir)
        self.text_extractor = TextExtractor()
        
        logger.info(f"--- [BrowserToPPTReplicator]: Initialized, output_dir: {self.output_dir}")
    
    async def replicate(
        self,
        html_content: str,
        output_ppt_path: Optional[Path] = None
    ) -> Path:
        """
        复刻HTML内容到PPT
        
        Args:
            html_content: HTML内容字符串（包含Ant Design组件）
            output_ppt_path: 输出PPT路径
            
        Returns:
            生成的PPT文件路径
        """
        logger.info("="*80)
        logger.info("--- [BrowserToPPTReplicator]: Starting replication process...")
        logger.info("="*80)
        
        # 1. 浏览器渲染
        logger.info("--- [Step 1/5]: Rendering HTML in browser...")
        browser_renderer = BrowserRenderer()
        page = await browser_renderer.render_html(html_content)
        
        try:
            # 2. 分析元素
            logger.info("--- [Step 2/5]: Analyzing page elements...")
            elements = await self.element_analyzer.analyze_elements(page)
            containers_info = elements['containers']
            texts_info = elements['texts']
            
            # 3. 提取容器（截图）
            # 【新架构原则】：使用混合渲染法，隐藏文字后截图
            logger.info("--- [Step 3/5]: Extracting containers (screenshots with hybrid rendering)...")
            containers = await self.container_extractor.extract_all_containers(
                containers_info, 
                hide_text=True  # 隐藏文字，用于混合渲染
            )
            
            # 4. 提取文本
            logger.info("--- [Step 4/5]: Extracting texts...")
            texts = await self.text_extractor.extract_all_texts(texts_info)
            
            # 5. 复刻到PPT（使用混合渲染法）
            logger.info("--- [Step 5/5]: Replicating to PPT (Hybrid Rendering)...")
            ppt_replicator = PPTReplicator(self.coordinate_mapper, output_ppt_path)
            ppt_replicator.replicate_slide(
                containers, 
                texts,
                use_hybrid_rendering=True  # 使用混合渲染：容器用图片，文本用原生
            )
            
            # 保存PPT
            output_path = ppt_replicator.save(output_ppt_path)
            
            logger.info("="*80)
            logger.info(f"--- [BrowserToPPTReplicator]: Replication completed!")
            logger.info(f"    Output PPT: {output_path}")
            logger.info(f"    Containers: {len(containers)}")
            logger.info(f"    Texts: {len(texts)}")
            logger.info("="*80)
            
            return output_path
            
        finally:
            # 关闭浏览器
            await browser_renderer.close()
    
    async def replicate_from_file(
        self,
        html_file_path: Path,
        output_ppt_path: Optional[Path] = None
    ) -> Path:
        """
        从HTML文件复刻到PPT
        
        Args:
            html_file_path: HTML文件路径
            output_ppt_path: 输出PPT路径
            
        Returns:
            生成的PPT文件路径
        """
        html_content = Path(html_file_path).read_text(encoding='utf-8')
        return await self.replicate(html_content, output_ppt_path)

