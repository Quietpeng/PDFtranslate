"""
PDF Translator
Author: @Quietpeng
GitHub: https://github.com/Quietpeng
Based on: @Byaidu/PDFMathTranslate
"""

import os
import argparse
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional
import sys
import requests
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_proxy():
    """设置代理"""
    try:
        # 尝试从环境变量获取代理设置
        proxy = os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')
        if not proxy:
            # 默认代理设置
            proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890'
            }
            # 尝试不同的常用代理端口
            ports = ['7890', '1080', '8080']
            for port in ports:
                os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
                os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
                if check_network():
                    logging.info(f"成功连接到代理(端口: {port})")
                    return True
            logging.warning("未能找到可用的代理，将尝试直接连接")
            return False
        return True
    except Exception as e:
        logging.warning(f"代理设置失败: {str(e)}")
        return False

def check_network():
    """检查网络连接"""
    try:
        # 设置较短的超时时间
        requests.get('https://huggingface.co', timeout=3)
        return True
    except:
        return False

def import_pdf2zh():
    """导入pdf2zh模块"""
    try:
        from pdf2zh import translate_stream
        return translate_stream
    except ImportError:
        logging.error("未找到pdf2zh模块，正在尝试安装...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pdf2zh"])
            from pdf2zh import translate_stream
            return translate_stream
        except Exception as e:
            logging.error(f"安装pdf2zh失败: {str(e)}")
            sys.exit(1)

# 设置代理并导入必要模块
setup_proxy()
translate_stream = import_pdf2zh()

class PDFTranslator:
    """PDF文档翻译器"""
    
    def __init__(self, lang_in: str = 'en', lang_out: str = 'zh', 
                 service: str = 'google', thread: int = 4):
        """初始化翻译器"""
        try:
            self.params = {
                'lang_in': lang_in,
                'lang_out': lang_out,
                'service': service,
                'thread': thread,
            }
        except Exception as e:
            logging.error(f"初始化翻译器失败: {str(e)}")
            raise

    def translate_file(self, file_path: str) -> Optional[bytes]:
        """翻译单个PDF文件"""
        try:
            logging.info(f"开始读取文件: {file_path}")
            with open(file_path, 'rb') as f:
                file_content = f.read()
                file_size = len(file_content) / (1024 * 1024)  # 转换为MB
                logging.info(f"文件大小: {file_size:.2f}MB")
                
                logging.info("正在翻译文件内容...")
                stream_mono, _ = translate_stream(stream=file_content, **self.params)
                
                translated_size = len(stream_mono) / (1024 * 1024)  # 转换为MB
                logging.info(f"翻译完成，输出文件大小: {translated_size:.2f}MB")
                return stream_mono
        except Exception as e:
            logging.error(f"翻译文件 {file_path} 时发生错误: {str(e)}")
            return None

    def list_pdf_files(self, directory: str) -> List[str]:
        """获取目录下所有PDF文件"""
        pdf_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files

    def translate_single(self, input_path: str, output_path: str) -> None:
        """翻译单个PDF文件"""
        if not os.path.exists(input_path):
            logging.error(f"文件不存在: {input_path}")
            return

        os.makedirs(output_path, exist_ok=True)
        filename = os.path.basename(input_path)
        output_file = os.path.join(output_path, f"{os.path.splitext(filename)[0]}_translated.pdf")

        logging.info(f"===== 开始翻译文件: {filename} =====")
        translated_content = self.translate_file(input_path)
        
        if translated_content:
            logging.info(f"正在保存翻译结果到: {output_file}")
            with open(output_file, 'wb') as f:
                f.write(translated_content)
            logging.info(f"===== 文件 {filename} 翻译完成 =====\n")
        else:
            logging.error(f"===== 文件 {filename} 翻译失败 =====\n")

    def translate_directory(self, input_dir: str, output_dir: str) -> None:
        """翻译目录下的所有PDF文件"""
        if not os.path.exists(input_dir):
            logging.error(f"目录不存在: {input_dir}")
            return

        pdf_files = self.list_pdf_files(input_dir)
        if not pdf_files:
            logging.warning(f"在 {input_dir} 中未找到PDF文件")
            return

        total_files = len(pdf_files)
        logging.info(f"找到 {total_files} 个PDF文件待翻译")
        
        os.makedirs(output_dir, exist_ok=True)
        
        for index, file_path in enumerate(tqdm(pdf_files, desc="总体进度")):
            logging.info(f"\n正在处理第 {index + 1}/{total_files} 个文件")
            self.translate_single(file_path, output_dir)
        
        logging.info(f"\n===== 所有文件翻译完成 =====")
        logging.info(f"成功翻译 {total_files} 个文件")
        logging.info(f"输出目录: {output_dir}\n")

class TranslatorGUI:
    """翻译器图形界面"""
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PDF Translator")
        self.window.geometry("600x500")
        
        self.languages = {
            '中文': 'zh',
            '英语': 'en',
            '日语': 'ja',
            '韩语': 'ko',
            '法语': 'fr',
            '德语': 'de',
            '俄语': 'ru'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置GUI界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 语言选择区域
        lang_frame = ttk.LabelFrame(main_frame, text="语言设置", padding="5")
        lang_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 源语言选择
        ttk.Label(lang_frame, text="源语言:").grid(row=0, column=0, padx=5)
        self.source_lang = ttk.Combobox(lang_frame, values=list(self.languages.keys()), width=15)
        self.source_lang.set('英语')
        self.source_lang.grid(row=0, column=1, padx=5)
        
        # 切换按钮
        ttk.Button(lang_frame, text="⇄", command=self.switch_languages, width=3).grid(row=0, column=2, padx=5)
        
        # 目标语言选择
        ttk.Label(lang_frame, text="目标语言:").grid(row=0, column=3, padx=5)
        self.target_lang = ttk.Combobox(lang_frame, values=list(self.languages.keys()), width=15)
        self.target_lang.set('中文')
        self.target_lang.grid(row=0, column=4, padx=5)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件设置", padding="5")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 输入文件/文件夹选择
        ttk.Label(file_frame, text="输入路径:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.input_path = ttk.Entry(file_frame, width=50)
        self.input_path.grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="选择文件", command=self.select_input_file).grid(row=0, column=2, padx=5)
        ttk.Button(file_frame, text="选择文件夹", command=self.select_input_dir).grid(row=0, column=3, padx=5)
        
        # 输出目录选择
        ttk.Label(file_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.output_path = ttk.Entry(file_frame, width=50)
        self.output_path.insert(0, "./翻译后output")
        self.output_path.grid(row=1, column=1, padx=5)
        ttk.Button(file_frame, text="选择目录", command=self.select_output_dir).grid(row=1, column=2, padx=5)
        
        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="翻译状态", padding="5")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_text = tk.Text(status_frame, height=10, width=60)
        self.status_text.grid(row=0, column=0, padx=5, pady=5)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.status_text['yscrollcommand'] = scrollbar.set
        
        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="开始翻译", command=self.start_translation).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="清除日志", command=self.clear_status).grid(row=0, column=1, padx=5)
        
    def switch_languages(self):
        """切换源语言和目标语言"""
        source = self.source_lang.get()
        target = self.target_lang.get()
        self.source_lang.set(target)
        self.target_lang.set(source)
        
    def select_input_file(self):
        """选择输入文件"""
        filename = filedialog.askopenfilename(
            title="选择PDF文件",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.delete(0, tk.END)
            self.input_path.insert(0, filename)
            
    def select_input_dir(self):
        """选择输入目录"""
        dirname = filedialog.askdirectory(title="选择输入目录")
        if dirname:
            self.input_path.delete(0, tk.END)
            self.input_path.insert(0, dirname)
            
    def select_output_dir(self):
        """选择输出目录"""
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_path.delete(0, tk.END)
            self.output_path.insert(0, dirname)
            
    def clear_status(self):
        """清除状态显示"""
        self.status_text.delete(1.0, tk.END)
        
    def add_status(self, message: str):
        """添加状态信息"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.window.update()
        
    def validate_paths(self) -> Optional[str]:
        """验证路径是否有效"""
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        
        if not input_path:
            return "请选择输入文件或目录"
            
        if not output_path:
            return "请选择输出目录"
            
        if os.path.isfile(input_path) and not input_path.lower().endswith('.pdf'):
            return "输入文件必须是PDF格式"
            
        return None
        
    def start_translation(self):
        """开始翻译"""
        error = self.validate_paths()
        if error:
            messagebox.showerror("错误", error)
            return
            
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        
        translator = PDFTranslator(
            lang_in=self.languages[self.source_lang.get()],
            lang_out=self.languages[self.target_lang.get()]
        )
        
        try:
            self.clear_status()  # 清除之前的状态
            if os.path.isfile(input_path):
                self.add_status(f"===== 开始翻译文件 =====")
                self.add_status(f"输入文件: {input_path}")
                self.add_status(f"输出目录: {output_path}\n")
                
                translator.translate_single(input_path, output_path)
                
                self.add_status("\n===== 翻译完成！=====")
            else:
                pdf_files = translator.list_pdf_files(input_path)
                total_files = len(pdf_files)
                
                self.add_status(f"===== 开始批量翻译 =====")
                self.add_status(f"输入目录: {input_path}")
                self.add_status(f"输出目录: {output_path}")
                self.add_status(f"待翻译文件数: {total_files}\n")
                
                for index, file_path in enumerate(pdf_files, 1):
                    self.add_status(f"正在翻译第 {index}/{total_files} 个文件: {os.path.basename(file_path)}")
                    translator.translate_single(file_path, output_path)
                
                self.add_status(f"\n===== 批量翻译完成！=====")
                self.add_status(f"共完成 {total_files} 个文件的翻译")
        except Exception as e:
            self.add_status(f"\n翻译过程中发生错误: {str(e)}")
            messagebox.showerror("错误", f"翻译失败: {str(e)}")
            
    def run(self):
        """运行GUI程序"""
        self.window.mainloop()

def main():
    """主函数"""
    # 检查环境
    if not check_network():
        logging.error("无法连接到网络，请检查网络连接")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='PDF文件翻译工具')
    parser.add_argument('-i', '--input', help='输入文件夹路径')
    parser.add_argument('-o', '--output', help='输出文件夹路径', default='./翻译后output')
    parser.add_argument('-s', '--single', help='单个PDF文件路径')

    args = parser.parse_args()

    try:
        # 如果有命令行参数，使用命令行模式
        if args.input or args.single:
            translator = PDFTranslator()
            if args.single:
                translator.translate_single(args.single, args.output)
            else:
                translator.translate_directory(args.input, args.output)
        # 否则启动GUI
        else:
            gui = TranslatorGUI()
            gui.run()
    except Exception as e:
        logging.error(f"程序运行出错: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()