-- 导出  表 db_831007526.dim_auction 结构
CREATE TABLE IF NOT EXISTS `dim_auction` (
  `createtime` date DEFAULT NULL COMMENT '创建日期',
  `updatetime` date DEFAULT NULL COMMENT '更新日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '卖家ID',
  `user_type` int(1) DEFAULT NULL COMMENT '店铺类型',
  `sellernick` varchar(255) DEFAULT NULL COMMENT '卖家旺旺',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `auction_title` varchar(255) DEFAULT NULL COMMENT '商品标题',
  `rank_score` float(7,6) DEFAULT NULL COMMENT '淘宝排名权重',
  `itemnum` varchar(255) DEFAULT NULL COMMENT '产品ID',
  `cat_id` bigint(20) DEFAULT NULL COMMENT '类目ID',
  `brand_id` bigint(20) DEFAULT NULL COMMENT '品牌ID',
  `quantity` bigint(20) DEFAULT NULL COMMENT '在线库存量',
  `price` decimal(15,2) DEFAULT NULL COMMENT 'PC端价格',
  `price_wap` decimal(15,2) DEFAULT NULL COMMENT '手机端价格',
  `min_price` decimal(15,2) DEFAULT NULL COMMENT 'ADD:PC端最低价',
  `min_price_wap` decimal(15,2) DEFAULT NULL COMMENT 'ADD:手机端最低价',
  `total_sold_quantity` bigint(20) DEFAULT NULL COMMENT '总售出数量',
  `recent_sold_quantity` bigint(20) DEFAULT NULL COMMENT '30天售出数量',
  `total_bookmark` bigint(20) DEFAULT NULL COMMENT '总收藏量',
  `is_reviewed_item` int(1) DEFAULT NULL COMMENT '是否人工审核过该商品货号信息等',
  UNIQUE KEY `auction_id` (`auction_id`),
  KEY `seller_id` (`seller_id`),
  KEY `user_type` (`user_type`),
  KEY `sellernick` (`sellernick`),
  KEY `cat_id` (`cat_id`),
  KEY `brand_id` (`brand_id`),
  KEY `rank_score` (`rank_score`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_auction_sku 结构
CREATE TABLE IF NOT EXISTS `dim_auction_sku` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `sku_id` varchar(50) NOT NULL DEFAULT '-1' COMMENT '商家编码',
  `auction_id` bigint(20) NOT NULL DEFAULT '-1' COMMENT '商品ID',
  `auction_title` varchar(255) DEFAULT NULL COMMENT '标题',
  `cat_id` bigint(20) DEFAULT NULL COMMENT '所属类目',
  PRIMARY KEY (`id`),
  UNIQUE KEY `itemnum` (`sku_id`),
  KEY `cat_id` (`cat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_brand 结构
CREATE TABLE IF NOT EXISTS `dim_brand` (
  `pid` bigint(20) NOT NULL DEFAULT '-1' COMMENT '归属ID',
  `props` varchar(50) NOT NULL DEFAULT '-1' COMMENT '标签归属',
  `vid2` bigint(20) NOT NULL DEFAULT '-1' COMMENT '此处为：品牌ID',
  `brand` varchar(255) NOT NULL DEFAULT '-1' COMMENT '品牌名称',
  UNIQUE KEY `vid2` (`vid2`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='品牌维度表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_customer 结构
CREATE TABLE IF NOT EXISTS `dim_customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `buyer_id` varchar(255) DEFAULT NULL COMMENT '平台计算脱敏特征值',
  `alipay_account` varchar(50) DEFAULT NULL,
  `buyer_id_md5` varchar(50) DEFAULT NULL COMMENT '买家MD5索引',
  `auction_count` bigint(21) NOT NULL DEFAULT '0' COMMENT '购买次数',
  `firstdate` date DEFAULT NULL COMMENT '首次购买时间',
  `lastdate` date DEFAULT NULL COMMENT '订单创建时间',
  `total_fee` double DEFAULT NULL COMMENT '总订单金额',
  `total_fee_failed` double DEFAULT NULL COMMENT '失败订单金额',
  `level` varchar(50) DEFAULT NULL COMMENT '客户标签',
  PRIMARY KEY (`id`),
  KEY `buyer_id_md5` (`buyer_id_md5`),
  KEY `auction_count` (`auction_count`),
  KEY `buyer_id` (`buyer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='客户维度表：由订单事实抽取计算得出';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_date 结构
CREATE TABLE IF NOT EXISTS `dim_date` (
  `dateindex` date NOT NULL COMMENT '日期',
  `year` int(4) NOT NULL COMMENT '年',
  `quarter` int(1) NOT NULL COMMENT '一年中的第几季度',
  `month` int(2) NOT NULL COMMENT '月份编号',
  `monthname` varchar(10) NOT NULL COMMENT '月份名称',
  `day` int(2) NOT NULL COMMENT '一月中的第几日',
  `dayname` varchar(2) NOT NULL COMMENT '日期名称',
  `dayofyear` int(3) NOT NULL COMMENT '一年中的第几日',
  `weekofyear` int(2) NOT NULL COMMENT '一年中的第几周',
  `dayofweek` int(1) NOT NULL COMMENT '一周中的第几日',
  `holiday` varchar(255) NOT NULL,
  UNIQUE KEY `updatetime` (`dateindex`),
  KEY `dayofmonth` (`day`),
  KEY `dayofyear` (`dayofyear`),
  KEY `dayofweek` (`dayofweek`),
  KEY `dayname` (`dayname`),
  KEY `weekofyear` (`weekofyear`),
  KEY `monthnumber` (`month`),
  KEY `monthname` (`monthname`),
  KEY `year` (`year`),
  KEY `quarter` (`quarter`),
  KEY `holiday` (`holiday`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='固定维度表：日期';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_device 结构
CREATE TABLE IF NOT EXISTS `dim_device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `devid` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `devid` (`devid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_ind_brand_sku 结构
CREATE TABLE IF NOT EXISTS `dim_ind_brand_sku` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cat_id` bigint(20) DEFAULT NULL COMMENT '类目ID',
  `brand_id` bigint(20) DEFAULT NULL COMMENT '品牌ID',
  `brand` varchar(100) DEFAULT NULL COMMENT '品牌名称',
  `sku` varchar(50) DEFAULT NULL COMMENT 'SKU属性',
  `skuid` bigint(20) DEFAULT NULL COMMENT 'SKUid',
  PRIMARY KEY (`id`),
  UNIQUE KEY `skuid` (`skuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_ind_people_p 结构
CREATE TABLE IF NOT EXISTS `dim_ind_people_p` (
  `pid` varchar(255) DEFAULT NULL,
  `props_value` varchar(255) DEFAULT NULL,
  UNIQUE KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_ind_people_v 结构
CREATE TABLE IF NOT EXISTS `dim_ind_people_v` (
  `theid` varchar(255) DEFAULT NULL,
  `pid` varchar(255) DEFAULT NULL,
  `props_value` varchar(255) DEFAULT NULL,
  `vid` int(11) DEFAULT NULL,
  `vid_value` varchar(255) DEFAULT NULL,
  UNIQUE KEY `theid` (`theid`),
  KEY `props_value` (`props_value`),
  KEY `pid` (`pid`),
  KEY `vid` (`vid`),
  KEY `vid_value` (`vid_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_itemcat 结构
CREATE TABLE IF NOT EXISTS `dim_itemcat` (
  `cat_id` bigint(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `parent_cid` bigint(20) DEFAULT NULL,
  `is_parent` varchar(10) DEFAULT NULL,
  `level` int(1) DEFAULT NULL,
  UNIQUE KEY `cid_unique` (`cat_id`),
  KEY `cid` (`cat_id`),
  KEY `level` (`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_itemcat_parent 结构
CREATE TABLE IF NOT EXISTS `dim_itemcat_parent` (
  `cat_id` bigint(20) DEFAULT NULL,
  `cat_name` varchar(50) DEFAULT NULL,
  `cat_l3_id` bigint(20) DEFAULT NULL,
  `cat_l3_name` varchar(50) DEFAULT NULL,
  `cat_l2_id` bigint(20) DEFAULT NULL,
  `cat_l2_name` varchar(50) DEFAULT NULL,
  `cat_l1_id` bigint(20) DEFAULT NULL,
  `cat_l1_name` varchar(50) DEFAULT NULL,
  `cat_l0_id` bigint(20) DEFAULT NULL,
  UNIQUE KEY `cat_id` (`cat_id`),
  KEY `cat_l3_id` (`cat_l3_id`),
  KEY `cat_l2_id` (`cat_l2_id`),
  KEY `cat_l1_id` (`cat_l1_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_keyword_item 结构
CREATE TABLE IF NOT EXISTS `dim_keyword_item` (
  `updatetime` date DEFAULT NULL,
  `seller_id` bigint(20) DEFAULT NULL,
  `keyword` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `tag_brand` varchar(50) DEFAULT NULL,
  `is_valid` int(1) NOT NULL DEFAULT '1',
  `ind_pv` bigint(20) NOT NULL DEFAULT '1',
  UNIQUE KEY `keyword` (`keyword`,`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_keyword_tag 结构
CREATE TABLE IF NOT EXISTS `dim_keyword_tag` (
  `keyword` varchar(50) DEFAULT NULL,
  `tag` varchar(50) DEFAULT NULL,
  `have_problem` bigint(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_price 结构
CREATE TABLE IF NOT EXISTS `dim_price` (
  `price` int(11) NOT NULL AUTO_INCREMENT,
  `D5` int(11) DEFAULT NULL,
  `D10` int(11) DEFAULT NULL,
  `D50` int(11) DEFAULT NULL,
  `D100` int(11) DEFAULT NULL,
  `D500` int(11) DEFAULT NULL,
  `D1000` int(11) DEFAULT NULL,
  PRIMARY KEY (`price`),
  KEY `price` (`price`),
  KEY `D10` (`D10`),
  KEY `D50` (`D50`),
  KEY `D100` (`D100`),
  KEY `D500` (`D500`),
  KEY `D1000` (`D1000`),
  KEY `D5` (`D5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_ratesum_buyer 结构
CREATE TABLE IF NOT EXISTS `dim_ratesum_buyer` (
  `ratesum` int(2) DEFAULT NULL,
  `ratesum_name` varchar(50) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  UNIQUE KEY `ratesum` (`ratesum`),
  KEY `rank` (`ratesum_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_ratesum_seller 结构
CREATE TABLE IF NOT EXISTS `dim_ratesum_seller` (
  `ratesum` int(2) DEFAULT NULL,
  `ratesum_name` varchar(50) DEFAULT NULL,
  `rank` varchar(50) DEFAULT NULL,
  UNIQUE KEY `ratesum` (`ratesum`),
  KEY `rank` (`ratesum_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_status_order_pay 结构
CREATE TABLE IF NOT EXISTS `dim_status_order_pay` (
  `pay_status` varchar(50) DEFAULT NULL,
  `pay_status_tag` varchar(50) DEFAULT NULL,
  UNIQUE KEY `pay_status` (`pay_status`),
  KEY `pay_status_tag` (`pay_status_tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单支付状态维度表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_tag 结构
CREATE TABLE IF NOT EXISTS `dim_tag` (
  `cid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL DEFAULT '-1' COMMENT '归属ID',
  `props` varchar(50) NOT NULL DEFAULT '-1' COMMENT '标签归属',
  `vid` bigint(20) NOT NULL DEFAULT '-1' COMMENT '标签ID',
  `value` varchar(255) NOT NULL DEFAULT '-1' COMMENT '标签内容',
  UNIQUE KEY `pid_vid` (`pid`,`vid`,`cid`),
  KEY `props` (`props`),
  KEY `value` (`value`),
  KEY `cid` (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_tag_auction_count 结构
CREATE TABLE IF NOT EXISTS `dim_tag_auction_count` (
  `auction_count` int(11) NOT NULL AUTO_INCREMENT,
  `auction_count_tag` int(11) DEFAULT NULL,
  `is_new` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`auction_count`),
  KEY `auction_count_tag` (`auction_count_tag`),
  KEY `is_new` (`is_new`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单订购次序维度表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_tag_auction_sub_days 结构
CREATE TABLE IF NOT EXISTS `dim_tag_auction_sub_days` (
  `auction_sub_days` int(11) NOT NULL AUTO_INCREMENT,
  `auction_sub_days_tag` varchar(50) DEFAULT NULL,
  `auction_sub_months_tag` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`auction_sub_days`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订购间隔天数维度表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_tag_province 结构
CREATE TABLE IF NOT EXISTS `dim_tag_province` (
  `province` varchar(50) DEFAULT NULL,
  UNIQUE KEY `province` (`province`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_time 结构
CREATE TABLE IF NOT EXISTS `dim_time` (
  `timeindex` varchar(24) DEFAULT NULL,
  `timehour` int(11) DEFAULT NULL,
  `timeminutes` int(11) DEFAULT NULL,
  UNIQUE KEY `timeindex_unique` (`timeindex`),
  KEY `timeindex` (`timeindex`),
  KEY `timehour` (`timehour`),
  KEY `timeminutes` (`timeminutes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='时间维度表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_trade_src 结构
CREATE TABLE IF NOT EXISTS `dim_trade_src` (
  `src_id` int(10) DEFAULT NULL COMMENT '流量来源ID',
  `src` varchar(255) DEFAULT NULL COMMENT '流量来源',
  `tag` varchar(255) DEFAULT NULL COMMENT '分组标签',
  UNIQUE KEY `src` (`src`),
  KEY `src_id` (`src_id`),
  KEY `tag` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.dim_user_type 结构
CREATE TABLE IF NOT EXISTS `dim_user_type` (
  `user_type` int(11) DEFAULT NULL,
  `user_type_name` varchar(50) DEFAULT NULL,
  KEY `user_type` (`user_type`),
  KEY `user_type_name` (`user_type_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.etc_cat_keyword 结构
CREATE TABLE IF NOT EXISTS `etc_cat_keyword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` bigint(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `devid` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.etc_download_sycm 结构
CREATE TABLE IF NOT EXISTS `etc_download_sycm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` text,
  `tag` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.etc_rule 结构
CREATE TABLE IF NOT EXISTS `etc_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `rule` text,
  `comment` varchar(255) DEFAULT NULL,
  `usage` varchar(255) DEFAULT NULL COMMENT '使用场景',
  UNIQUE KEY `name` (`name`),
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.fact_ind_keyword_uv 结构
CREATE TABLE IF NOT EXISTS `fact_ind_keyword_uv` (
  `thedate` date DEFAULT NULL COMMENT '日期',
  `devid` varchar(50) DEFAULT NULL COMMENT '来源',
  `cat_id` bigint(20) DEFAULT NULL COMMENT '所属类目',
  `keyword` varchar(255) DEFAULT NULL COMMENT '搜索词',
  `pv` bigint(20) DEFAULT NULL COMMENT '全网搜索热度',
  `click_rate` float(15,4) DEFAULT NULL COMMENT '全网点击率',
  `auction_num` bigint(20) DEFAULT NULL COMMENT '全网商品数',
  `trade_rate` float(15,4) DEFAULT NULL COMMENT '全网转化率',
  `tmall_click_rate` float(15,4) DEFAULT NULL COMMENT '商城点击占比',
  `id` int(11) DEFAULT NULL COMMENT '文件截取ID',
  `id_b` int(11) DEFAULT NULL COMMENT '读取ID',
  `short_filename` varchar(255) DEFAULT NULL COMMENT '文件名',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间戳',
  UNIQUE KEY `thedate_cat_id_keyword` (`thedate`,`cat_id`,`keyword`,`devid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.fact_ind_people 结构
CREATE TABLE IF NOT EXISTS `fact_ind_people` (
  `thedate` date DEFAULT NULL COMMENT '日期',
  `skuid` varchar(255) DEFAULT NULL COMMENT '所属分类标签',
  `theid` varchar(50) DEFAULT NULL COMMENT '唯一索引=pid&''-''&vid',
  `pid` varchar(255) DEFAULT NULL COMMENT '属性',
  `vid` int(11) DEFAULT NULL COMMENT '属性参数',
  `value` bigint(20) DEFAULT NULL COMMENT '数据',
  UNIQUE KEY `thedate_skuid_theid` (`thedate`,`skuid`,`theid`),
  KEY `theid` (`theid`),
  KEY `skuid` (`skuid`),
  KEY `thedate` (`thedate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.fact_ind_search 结构
CREATE TABLE IF NOT EXISTS `fact_ind_search` (
  `thedate` date DEFAULT NULL COMMENT '时间：年/月/日',
  `cat_id` bigint(20) DEFAULT NULL COMMENT '类目ID',
  `search_index` int(11) DEFAULT NULL COMMENT '玻璃杯淘宝搜索指数',
  UNIQUE KEY `thedate_cat_id` (`thedate`,`cat_id`),
  KEY `thedate` (`thedate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.fact_shop_keyword 结构
CREATE TABLE IF NOT EXISTS `fact_shop_keyword` (
  `thedate` date DEFAULT NULL COMMENT '日期',
  `keyword` varchar(255) DEFAULT NULL COMMENT '关键词',
  `cat_id` bigint(20) DEFAULT NULL COMMENT '关键词所属类目ID',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `ind_pv` bigint(20) DEFAULT NULL COMMENT '行业搜索浏览量',
  `ind_auction_num` bigint(20) DEFAULT NULL COMMENT '行业可搜索商品总数',
  `shop_expose` bigint(20) DEFAULT NULL COMMENT '店铺商品曝光',
  `shop_pv` bigint(20) DEFAULT NULL COMMENT '店铺商品浏览量',
  `shop_uv` bigint(20) DEFAULT NULL COMMENT '店铺商品访客',
  `shop_out_rate` bigint(20) DEFAULT NULL COMMENT '店铺商品访客跳失率',
  `auction_cnt` bigint(20) DEFAULT NULL COMMENT '该关键词的总曝光关键词',
  `shop_expose_sum` bigint(20) DEFAULT NULL COMMENT '该关键词的店铺总曝光',
  `shop_pv_sum` bigint(20) DEFAULT NULL COMMENT '该关键词的店铺总浏览量',
  UNIQUE KEY `unique_indx` (`thedate`,`keyword`,`cat_id`,`auction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.fact_shop_order 结构
CREATE TABLE IF NOT EXISTS `fact_shop_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
  `thedate` date DEFAULT NULL COMMENT '订单创建时间',
  `thedate_last` date DEFAULT NULL COMMENT '上一次订单创建时间',
  `order_id` varchar(50) NOT NULL DEFAULT '-1' COMMENT 'T:订单ID',
  `parent_order_id` varchar(50) NOT NULL DEFAULT '-1' COMMENT 'T:交易ID',
  `seller_id` bigint(20) NOT NULL DEFAULT '-1' COMMENT 'T:卖家UID',
  `shop_id` bigint(20) NOT NULL DEFAULT '-1' COMMENT '店铺Id',
  `auction_count` int(11) DEFAULT NULL COMMENT '购买次序',
  `auction_sub_days` int(11) DEFAULT NULL COMMENT '距上次购买天数',
  `buyer_id` varchar(255) DEFAULT NULL COMMENT '用户名：平台计算脱敏特征值',
  `buyer_id_md5` varchar(255) DEFAULT NULL COMMENT '旺旺ID MD5',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `sku_id` varchar(50) NOT NULL DEFAULT '-1' COMMENT '商品货号',
  `gmv_time` datetime DEFAULT NULL COMMENT '拍下时间',
  `gmv_date` date DEFAULT NULL COMMENT 'T:拍下日期',
  `gmv_hour` varchar(50) DEFAULT NULL COMMENT 'T:拍下小时',
  `gmv_auction_num` bigint(20) DEFAULT NULL COMMENT '拍下订单总件数',
  `gmv_trade_amt` float(16,2) DEFAULT NULL COMMENT '拍下订单金额',
  `pay_time` datetime DEFAULT NULL COMMENT 'T:支付时间',
  `pay_date` date DEFAULT NULL COMMENT 'T:支付日期',
  `pay_hour` varchar(50) DEFAULT NULL COMMENT 'T:支付小时',
  `pay_amt` float(16,2) DEFAULT NULL COMMENT '成功支付金额',
  `order_status` varchar(50) DEFAULT NULL COMMENT 'T:交易状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `thedate_order_id_seller_id` (`order_id`),
  KEY `thedate` (`thedate`),
  KEY `thedate_last` (`thedate_last`),
  KEY `order_id` (`order_id`),
  KEY `seller_id` (`seller_id`),
  KEY `shop_id` (`shop_id`),
  KEY `auction_count` (`auction_count`),
  KEY `auction_sub_days` (`auction_sub_days`),
  KEY `buyer_id` (`buyer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单事实表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_crawl_shop_item 结构
CREATE TABLE IF NOT EXISTS `raw_crawl_shop_item` (
  `updatetime` date DEFAULT NULL COMMENT '数据更新日期',
  `uid` bigint(20) DEFAULT NULL COMMENT '用户id',
  `sellernick` varchar(50) DEFAULT NULL COMMENT '卖家昵称',
  `user_type` int(1) DEFAULT NULL COMMENT '是否卖家',
  `ratesum` int(5) DEFAULT NULL COMMENT '卖家等级',
  `itemid` bigint(20) DEFAULT NULL COMMENT '产品ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `old_starts` date DEFAULT NULL COMMENT '宝贝创建日期',
  `bid` bigint(20) DEFAULT NULL COMMENT '品牌ID',
  `cid` bigint(20) DEFAULT NULL COMMENT '类目ID',
  `price` int(11) DEFAULT NULL COMMENT '折算价格(已四舍五入)',
  `shipping_fee` decimal(15,2) DEFAULT NULL COMMENT '邮费',
  `dsr_desc` decimal(5,2) DEFAULT NULL COMMENT '描述评分',
  `ordercost` int(11) DEFAULT NULL COMMENT '宝贝收藏量',
  `people_num` int(11) DEFAULT NULL COMMENT '客户数',
  `total_sold_quantity` int(11) DEFAULT NULL COMMENT '总销量',
  `quantity` int(11) DEFAULT NULL COMMENT '库存',
  `biz30day` int(11) DEFAULT NULL COMMENT '30天成交件数',
  `comment_count` int(11) DEFAULT NULL COMMENT '评价数量',
  `volume30day` int(11) DEFAULT NULL COMMENT '30天售出',
  `total_fee` int(11) DEFAULT NULL COMMENT '估算成交额',
  `startdate_date` date DEFAULT NULL COMMENT '上架日期',
  `startdate_hour` varchar(4) DEFAULT NULL COMMENT '上架小时',
  `cc_score1` decimal(15,7) DEFAULT NULL COMMENT '综合排名',
  `pidvid` blob COMMENT '属性ID组',
  `vip` int(11) DEFAULT NULL COMMENT '支持vip折扣',
  `zk_final_price` decimal(15,2) DEFAULT NULL COMMENT '最高售价',
  `zk_final_price_wap` decimal(15,4) DEFAULT NULL COMMENT '手机售价',
  `ext_pict_url` varchar(255) DEFAULT NULL COMMENT '图片地址',
  UNIQUE KEY `itemid` (`itemid`,`updatetime`),
  KEY `uid` (`uid`),
  KEY `sellernick` (`sellernick`),
  KEY `user_type` (`user_type`),
  KEY `ratesum` (`ratesum`),
  KEY `old_starts` (`old_starts`),
  KEY `bid` (`bid`),
  KEY `cid` (`cid`),
  KEY `price` (`price`),
  KEY `startdate_date` (`startdate_date`),
  KEY `startdate_hour` (`startdate_hour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_crawl_shop_list 结构
CREATE TABLE IF NOT EXISTS `raw_crawl_shop_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updatetime` date DEFAULT NULL,
  `pageno` int(11) DEFAULT NULL,
  `shopid` bigint(20) DEFAULT NULL,
  `sellernick` varchar(50) DEFAULT NULL,
  `shopname` varchar(255) DEFAULT NULL,
  `shoptype` enum('-1','0','1') NOT NULL DEFAULT '-1',
  `mainsell` varchar(255) DEFAULT NULL,
  `maincat` varchar(50) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `sales` int(11) DEFAULT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `uid_encrypted` varchar(50) NOT NULL DEFAULT '-1',
  `rank` varchar(255) DEFAULT NULL,
  `itemnew` int(11) DEFAULT NULL,
  `itempromo` int(11) DEFAULT NULL,
  `ratenumber` int(11) DEFAULT NULL,
  `rate` float(15,5) DEFAULT NULL,
  `goodcomment` float(5,4) DEFAULT NULL,
  `dsr_desc` float(5,4) DEFAULT NULL,
  `dsr_srv` float(5,4) unsigned zerofill DEFAULT NULL,
  `dsr_ship` float(5,4) DEFAULT NULL,
  `mg` float(5,4) DEFAULT NULL,
  `sg` float(5,4) DEFAULT NULL,
  `cg` float(5,4) DEFAULT NULL,
  `keyword` varchar(50) DEFAULT NULL,
  `is_valid` enum('-1','0','1','2') DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `shopid_updatetime` (`shopid`),
  KEY `monthsales` (`sales`),
  KEY `sellernick` (`sellernick`),
  KEY `shoptype` (`shoptype`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='e-corp.cn';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_collect 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_collect` (
  `thedate` date DEFAULT NULL COMMENT '更新日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '商家ID',
  `shop_collect_num` bigint(20) DEFAULT NULL COMMENT '店铺收藏次数',
  `auction_collect_num` bigint(20) DEFAULT NULL COMMENT '商品收藏次数',
  `auction_collect_user_num` bigint(20) DEFAULT NULL COMMENT '商品收藏人数',
  `shop_collect_user_num` bigint(20) DEFAULT NULL COMMENT '店铺收藏人数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_dsr 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_dsr` (
  `thedate` date DEFAULT NULL COMMENT '统计日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '卖家ID',
  `dsr_low_score_user_num` bigint(20) DEFAULT NULL COMMENT 'DSR综合低评分买家数',
  `dsr_srv` float(6,5) DEFAULT NULL COMMENT '服务态度动态评分(DSR)',
  `dsr_desc` float(6,5) DEFAULT NULL COMMENT '描述相符动态评分(DSR)',
  `dsr_ship` float(6,5) DEFAULT NULL COMMENT '物流服务动态评分(DSR)',
  `refund_amt` float(15,4) DEFAULT NULL COMMENT '申请退款金额',
  `refund_user_num` bigint(20) DEFAULT NULL COMMENT '申请退款买家数',
  `order_shipped_cnt` bigint(20) DEFAULT NULL COMMENT '已发货父订单数',
  UNIQUE KEY `thedate_seller_id` (`thedate`,`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_item_keyword 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_item_keyword` (
  `thedate` date DEFAULT NULL COMMENT '日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '唯一识别',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `keyword` varchar(255) DEFAULT NULL COMMENT '关键词',
  `rank` int(11) DEFAULT NULL COMMENT '关键词排名',
  `expose` bigint(20) DEFAULT NULL COMMENT '曝光次数',
  `click_count` bigint(20) DEFAULT NULL COMMENT '点击次数',
  `click_rate` float(5,4) DEFAULT NULL COMMENT '点击率',
  `pv` bigint(20) DEFAULT NULL COMMENT '浏览量',
  `uv` bigint(20) DEFAULT NULL COMMENT '访客数',
  `avg_pv` float(15,2) DEFAULT NULL COMMENT '人均浏览量',
  `out_rate` float(5,4) DEFAULT NULL COMMENT '跳失率',
  `trade_user_num` bigint(20) DEFAULT NULL COMMENT '购买人数',
  `pay_auction_num` bigint(20) DEFAULT NULL COMMENT '支付件数',
  `pay_amt` float(15,4) DEFAULT NULL COMMENT '支付金额',
  `pay_rate` float(5,4) DEFAULT NULL COMMENT '支付转化率',
  `id` bigint(20) DEFAULT NULL COMMENT '文件ID',
  `join_id` bigint(20) DEFAULT NULL COMMENT '数据库ID',
  `short_filename` varchar(255) DEFAULT NULL COMMENT '导入文件名',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间戳',
  UNIQUE KEY `thedate_seller_id_auction_id_keyword` (`thedate`,`seller_id`,`auction_id`,`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_item_sum 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_item_sum` (
  `thedate` date DEFAULT NULL COMMENT '统计日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '商家ID',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `devid` varchar(50) DEFAULT NULL COMMENT '所属终端',
  `pv` bigint(20) DEFAULT NULL COMMENT '商品浏览量',
  `uv` bigint(20) DEFAULT NULL COMMENT '商品访客数',
  `page_duration` float(15,4) DEFAULT NULL COMMENT '人均停留时长',
  `out_rate` float(5,4) DEFAULT NULL COMMENT '日均跳出率',
  `trade_rate` float(5,4) DEFAULT NULL COMMENT '下单转化率',
  `trade_pay_rate` float(5,4) DEFAULT NULL COMMENT '下单-支付转化率',
  `pay_rate` float(5,4) DEFAULT NULL COMMENT '支付转化率',
  `trade_amt` float(15,4) DEFAULT NULL COMMENT '下单金额',
  `trade_auction_num` bigint(20) DEFAULT NULL COMMENT '下单商品件数',
  `trade_user_num` bigint(20) DEFAULT NULL COMMENT '下单买家数',
  `pay_amt` float(15,4) DEFAULT NULL COMMENT '支付金额',
  `pay_auction_num` bigint(20) DEFAULT NULL COMMENT '支付商品件数',
  `pay_user_num` bigint(20) DEFAULT NULL COMMENT '支付买家数',
  `add_cart_user_num` bigint(20) DEFAULT NULL COMMENT '加购件数',
  `collect_cnt` bigint(20) DEFAULT NULL COMMENT '收藏数',
  `avg_value` float(15,4) DEFAULT NULL COMMENT '访客平均价值',
  `search_pay_rate` float(5,4) DEFAULT NULL COMMENT '搜索支付转化率',
  `id` bigint(20) DEFAULT NULL COMMENT '文件ID',
  `join_id` bigint(20) DEFAULT NULL COMMENT '数据库ID',
  `short_filename` varchar(255) DEFAULT NULL COMMENT '导入文件名',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间戳',
  UNIQUE KEY `the_unique_index` (`thedate`,`seller_id`,`auction_id`,`devid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_item_uvsrc 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_item_uvsrc` (
  `thedate` date DEFAULT NULL COMMENT '日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '商家ID',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `src` varchar(255) DEFAULT NULL COMMENT '名称',
  `devid` varchar(50) DEFAULT NULL COMMENT 'PC_无线',
  `uv` float(15,4) DEFAULT NULL COMMENT '带来日均访客数',
  `uv_percent` float(5,4) DEFAULT NULL COMMENT '带来日均访客数占比',
  `uv_avg` float(15,4) DEFAULT NULL COMMENT '本店其他页面日均访客数',
  `uv_out` float(15,4) DEFAULT NULL COMMENT '跳出本店日均访客数',
  `trade_uv` float(15,4) DEFAULT NULL COMMENT '下单页面日均访客数',
  `add_cart_uv` float(15,4) DEFAULT NULL COMMENT '购物车日均访客数',
  `add_collect_uv` float(15,4) DEFAULT NULL COMMENT '收藏日均访客数',
  `id` bigint(20) DEFAULT NULL COMMENT '文件排序ID',
  `join_id` bigint(20) DEFAULT NULL COMMENT '数据库ID',
  `short_filename` varchar(255) DEFAULT NULL COMMENT '导入文件名',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间戳',
  UNIQUE KEY `thedate_seller_id_auction_id_src` (`thedate`,`seller_id`,`auction_id`,`src`,`devid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_order_sum 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_order_sum` (
  `thedate` date DEFAULT NULL COMMENT '统计日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '卖家ID',
  `avg_user_amt` float(15,4) DEFAULT NULL COMMENT '客单价',
  `trade_repeat_num` bigint(20) DEFAULT NULL COMMENT '老买家数',
  `trade_repeat_num_percent` float(5,4) DEFAULT NULL COMMENT '老买家数占比',
  `trade_pc_num` bigint(20) DEFAULT NULL COMMENT 'PC端下单买家数',
  `trade_pc_num_rate` float(5,4) DEFAULT NULL COMMENT 'PC端下单转化率',
  `pay_pc_num` bigint(20) DEFAULT NULL COMMENT 'PC端支付买家数',
  `pay_pc_repeat_num` bigint(20) DEFAULT NULL COMMENT 'PC端支付老买家数',
  `pay_pc_num_rate` float(5,4) DEFAULT NULL COMMENT 'PC端支付转化率',
  `pay_avg_auction_num_cnt` bigint(20) DEFAULT NULL COMMENT '人均支付商品件数',
  `auctioun_pay_num_rate` float(15,4) DEFAULT NULL COMMENT '商品详情页支付转化率',
  `wireless_user_avg_amt` float(15,4) DEFAULT NULL COMMENT '无线端客单价',
  `trade_wireless_amt` float(15,4) DEFAULT NULL COMMENT '无线端下单金额',
  `trade_wireless_num` bigint(20) DEFAULT NULL COMMENT '无线端下单买家数',
  `trade_wireless_num_rate` float(5,4) DEFAULT NULL COMMENT '无线端下单转化率',
  `pay_wireless_num` bigint(20) DEFAULT NULL COMMENT '无线端支付买家数',
  `pay_wireless_repeat_num` bigint(20) DEFAULT NULL COMMENT '无线端支付老买家数',
  `pay_wireless_num_percent` float(15,4) DEFAULT NULL COMMENT '无线端支付买家数占比',
  `pay_wireless_num_rate` float(15,4) DEFAULT NULL COMMENT '无线端支付转化率',
  `pay_wireless_auction_num_cnt` bigint(20) DEFAULT NULL COMMENT '无线端支付商品件数',
  `pay_wireless_auction_cnt` bigint(20) DEFAULT NULL COMMENT '无线端支付商品数',
  `pay_amt` float(15,4) DEFAULT NULL COMMENT '支付金额',
  `pay_user_num` bigint(20) DEFAULT NULL COMMENT '支付买家数',
  `trade_user_num_rate` float(5,4) DEFAULT NULL COMMENT '下单转化率',
  `pay_new_num` bigint(20) DEFAULT NULL COMMENT '新买家数',
  `pay_user_num_rate` float(5,4) DEFAULT NULL COMMENT '支付转化率',
  UNIQUE KEY `thedate_seller_id` (`thedate`,`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_uv 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_uv` (
  `thedate` date DEFAULT NULL COMMENT '统计日期',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '商家ID',
  `pv_auction_cnt` bigint(20) DEFAULT NULL COMMENT '被浏览商品数',
  `uv_homepage` bigint(20) DEFAULT NULL COMMENT '店铺首页访客数',
  `uv` bigint(20) DEFAULT NULL COMMENT '访客数',
  `repeat_uv` bigint(20) DEFAULT NULL COMMENT '老访客数',
  `pc_uv` bigint(20) DEFAULT NULL COMMENT 'PC端访客数',
  `pc_repeat_uv` bigint(20) DEFAULT NULL COMMENT 'PC端老访客数',
  `pc_bounce_rate` float(15,4) DEFAULT NULL COMMENT 'PC端跳失率',
  `pc_auction_uv` bigint(20) DEFAULT NULL COMMENT 'PC端商品详情页访客数',
  `pv_avg` float(15,4) DEFAULT NULL COMMENT '人均浏览量（访问深度）',
  `wireless_uv` bigint(20) DEFAULT NULL COMMENT '无线端访客数',
  `wireless_bounce_rate` float(15,4) DEFAULT NULL COMMENT '无线端跳失率',
  `new_uv` bigint(20) DEFAULT NULL COMMENT '新访客数',
  `wireless_auction_uv` bigint(20) DEFAULT NULL COMMENT '无线端商品详情页访客数',
  `wireless_uv_percent` float(15,4) DEFAULT NULL COMMENT '无线端访客数占比',
  `wireless_avg_page_duration` float(15,4) DEFAULT NULL COMMENT '无线端人均停留时长(秒)',
  `wireless_pv_avg` float(15,4) DEFAULT NULL COMMENT '无线端人均浏览量',
  `wireless_auction_pv` bigint(20) DEFAULT NULL COMMENT '无线端商品详情页浏览量',
  `repeat_uv_percent` float(15,4) DEFAULT NULL COMMENT '老访客数占比',
  `pv` bigint(20) DEFAULT NULL COMMENT '浏览量',
  UNIQUE KEY `thedate_seller_id` (`thedate`,`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_fact_shop_zhitongche_keyword 结构
CREATE TABLE IF NOT EXISTS `raw_fact_shop_zhitongche_keyword` (
  `seller_id` bigint(20) DEFAULT NULL,
  `thedate` date DEFAULT NULL,
  `nick` varchar(50) DEFAULT NULL,
  `customerId` bigint(20) DEFAULT NULL,
  `campaignId` bigint(20) DEFAULT NULL,
  `adgroupId` bigint(20) DEFAULT NULL,
  `keywordId` bigint(20) DEFAULT NULL,
  `word` varchar(255) DEFAULT NULL,
  `normalWord` varchar(255) DEFAULT NULL,
  `maxPrice` float(15,2) DEFAULT NULL,
  `isDefaultPrice` int(11) DEFAULT NULL,
  `auditState` int(11) DEFAULT NULL,
  `auditDesc` varchar(50) DEFAULT NULL,
  `auditTime` bigint(20) DEFAULT NULL,
  `isGarbage` int(11) DEFAULT NULL,
  `createTime` bigint(20) DEFAULT NULL,
  `lastUpdateTime` bigint(20) DEFAULT NULL,
  `excludeAdGroupId` varchar(255) DEFAULT NULL,
  `planDeleteTime` varchar(255) DEFAULT NULL,
  `wordType` int(11) DEFAULT NULL,
  `onlineFlag` int(11) DEFAULT NULL,
  `matchScope` int(11) DEFAULT NULL,
  `qscore` varchar(255) DEFAULT NULL,
  `sensitiveXml` varchar(256) DEFAULT NULL,
  `lawlessWords` varchar(257) DEFAULT NULL,
  `adGroupDTO` varchar(258) DEFAULT NULL,
  `minPrice` varchar(259) DEFAULT NULL,
  `checkWordDTO` varchar(260) DEFAULT NULL,
  `defaultPrice` varchar(261) DEFAULT NULL,
  `queryType` varchar(262) DEFAULT NULL,
  `averagePrice` varchar(263) DEFAULT NULL,
  `srcType` varchar(264) DEFAULT NULL,
  `campBidwordId` varchar(265) DEFAULT NULL,
  `itemId` varchar(266) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_keyword_crawl_shop_item 结构
CREATE TABLE IF NOT EXISTS `raw_keyword_crawl_shop_item` (
  `updatetime` date DEFAULT NULL COMMENT '数据更新日期',
  `keyword` varchar(255) DEFAULT NULL COMMENT '搜索关键词',
  `uid` bigint(20) DEFAULT NULL COMMENT '用户id',
  `sellernick` varchar(50) DEFAULT NULL COMMENT '卖家昵称',
  `user_type` int(1) DEFAULT NULL COMMENT '是否卖家',
  `ratesum` int(5) DEFAULT NULL COMMENT '卖家等级',
  `itemid` bigint(20) DEFAULT NULL COMMENT '产品ID',
  `title` varchar(255) DEFAULT NULL COMMENT '标题',
  `old_starts` date DEFAULT NULL COMMENT '宝贝创建日期',
  `bid` bigint(20) DEFAULT NULL COMMENT '品牌ID',
  `cid` bigint(20) DEFAULT NULL COMMENT '类目ID',
  `price` int(11) DEFAULT NULL COMMENT '折算价格(已四舍五入)',
  `shipping_fee` decimal(15,2) DEFAULT NULL COMMENT '邮费',
  `dsr_desc` decimal(5,2) DEFAULT NULL COMMENT '描述评分',
  `ordercost` int(11) DEFAULT NULL COMMENT '宝贝收藏量',
  `people_num` int(11) DEFAULT NULL COMMENT '客户数',
  `total_sold_quantity` int(11) DEFAULT NULL COMMENT '总销量',
  `quantity` int(11) DEFAULT NULL COMMENT '库存',
  `biz30day` int(11) DEFAULT NULL COMMENT '30天成交件数',
  `comment_count` int(11) DEFAULT NULL COMMENT '评价数量',
  `volume30day` int(11) DEFAULT NULL COMMENT '30天售出',
  `total_fee` int(11) DEFAULT NULL COMMENT '估算成交额',
  `startdate_date` date DEFAULT NULL COMMENT '上架日期',
  `startdate_hour` varchar(4) DEFAULT NULL COMMENT '上架小时',
  `cc_score1` decimal(15,7) DEFAULT NULL COMMENT '综合排名',
  `pidvid` blob COMMENT '属性ID组',
  `vip` int(11) DEFAULT NULL COMMENT '支持vip折扣',
  `zk_final_price` decimal(15,2) DEFAULT NULL COMMENT '最高售价',
  `zk_final_price_wap` decimal(15,4) DEFAULT NULL COMMENT '手机售价',
  `ext_pict_url` varchar(255) DEFAULT NULL COMMENT '图片地址',
  UNIQUE KEY `itemid` (`itemid`,`updatetime`,`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_order 结构
CREATE TABLE IF NOT EXISTS `raw_order` (
  `order_id` bigint(20) NOT NULL DEFAULT '-1' COMMENT '订单编号',
  `itemnum` varchar(50) NOT NULL DEFAULT '-1' COMMENT '商家编码',
  `item_title` varchar(255) DEFAULT NULL COMMENT '标题',
  `item_price` float(16,2) DEFAULT NULL COMMENT '价格',
  `item_num` int(11) DEFAULT NULL COMMENT '购买数量',
  `itemnum_outer_id` varchar(50) DEFAULT NULL COMMENT '外部系统编号',
  `sku` varchar(50) DEFAULT NULL COMMENT '商品属性',
  `auction_info` varchar(50) DEFAULT NULL COMMENT '套餐信息',
  `msg` text COMMENT '备注',
  `trade_status` varchar(50) DEFAULT NULL COMMENT '订单状态',
  PRIMARY KEY (`order_id`,`itemnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基础表：上传子订单/商品表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_shop_order 结构
CREATE TABLE IF NOT EXISTS `raw_shop_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thedate` date DEFAULT NULL COMMENT '统计日期',
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新日期',
  `order_id` varchar(255) DEFAULT NULL COMMENT '订单ID',
  `parent_order_id` varchar(255) DEFAULT NULL COMMENT '父订单ID',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '卖家ID',
  `shop_id` bigint(20) DEFAULT NULL COMMENT '店铺Id',
  `buyer_id` varchar(255) DEFAULT NULL COMMENT '买家ID',
  `auction_id` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `sku_id` varchar(255) DEFAULT NULL COMMENT 'SKU_ID',
  `gmv_trade_amt` double DEFAULT NULL COMMENT '订单提交金额',
  `gmv_auction_num` bigint(20) DEFAULT NULL COMMENT '提交商品件数',
  `pay_amt` double DEFAULT NULL COMMENT '成功下单金额',
  `order_status` varchar(50) DEFAULT NULL COMMENT '订单状态',
  `gmv_time` datetime DEFAULT NULL COMMENT '下单时间',
  `pay_time` datetime DEFAULT NULL COMMENT '订单支付时间',
  `data_src` varchar(50) DEFAULT NULL COMMENT '数据来源',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `thedate` (`thedate`),
  KEY `seller_id` (`seller_id`),
  KEY `buyer_id` (`buyer_id`),
  KEY `sku_id` (`sku_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='第三方_阿里_京东_数据平台导入数据_订单';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_trade 结构
CREATE TABLE IF NOT EXISTS `raw_trade` (
  `order_id` bigint(20) NOT NULL DEFAULT '-1' COMMENT '订单编号',
  `buyer_nick` varchar(255) DEFAULT NULL COMMENT '买家会员名',
  `seller_id` bigint(20) DEFAULT NULL COMMENT '卖家名称',
  `alipay_account` varchar(50) DEFAULT NULL COMMENT '买家支付宝账号',
  `gmv_trade_amt` float(16,2) DEFAULT NULL COMMENT '买家应付货款',
  `gmv_shipping_amt` float(16,2) DEFAULT NULL COMMENT '买家应付邮费',
  `gmv_trade_point` int(11) DEFAULT NULL COMMENT '买家支付积分',
  `gmv_total_amt` float(16,2) DEFAULT NULL COMMENT '总金额',
  `refund_trade_point` int(11) DEFAULT NULL COMMENT '返点积分',
  `alipay_trade_amt` float(16,2) DEFAULT NULL COMMENT '买家实际支付金额',
  `alipay_trade_point` int(11) DEFAULT NULL COMMENT '买家实际支付积分',
  `pay_status` varchar(50) DEFAULT NULL COMMENT '订单状态',
  `buyer_msg` text COMMENT '买家留言',
  `buyer_name` varchar(50) DEFAULT NULL COMMENT '收货人姓名',
  `buyer_address` varchar(255) DEFAULT NULL COMMENT '收货地址 ',
  `gmv_deliver_type` varchar(50) DEFAULT NULL COMMENT '运送方式',
  `buyer_phone` varchar(50) DEFAULT NULL COMMENT '联系电话 ',
  `buyer_mobile_phone` varchar(50) DEFAULT NULL COMMENT '联系手机',
  `gmv_time` datetime DEFAULT NULL COMMENT '订单创建时间',
  `alipay_time` datetime DEFAULT NULL COMMENT '订单付款时间 ',
  `item_title_collection` text COMMENT '宝贝标题 ',
  `gmv_category_num` int(11) DEFAULT NULL COMMENT '宝贝种类数',
  `gmv_auction_num` int(11) DEFAULT NULL COMMENT '宝贝总件数',
  `deliver_no` varchar(50) DEFAULT NULL COMMENT '物流单号 ',
  `deliver_company` varchar(50) DEFAULT NULL COMMENT '物流公司',
  `seller_msg` text COMMENT '订单备注',
  `shop_id` bigint(20) DEFAULT NULL COMMENT '店铺Id',
  `shop_name` varchar(50) DEFAULT NULL COMMENT '店铺名称',
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='基础表：上传交易表';

-- 数据导出被取消选择。


-- 导出  表 db_831007526.raw_trade_comment 结构
CREATE TABLE IF NOT EXISTS `raw_trade_comment` (
  `updatetime` date DEFAULT NULL COMMENT '数据更新日期',
  `createtime` datetime DEFAULT NULL COMMENT '记录创建时间',
  `tid` bigint(20) DEFAULT NULL COMMENT '交易ID',
  `oid` bigint(20) DEFAULT NULL COMMENT '订单ID',
  `itemid` bigint(20) DEFAULT NULL COMMENT '商品ID',
  `title` varchar(255) DEFAULT NULL COMMENT '商品标题',
  `price` float(15,2) DEFAULT NULL COMMENT '商品价格',
  `nick` varchar(50) DEFAULT NULL COMMENT '旺旺昵称',
  `role` varchar(50) DEFAULT NULL COMMENT '旺旺角色',
  `result` varchar(10) DEFAULT NULL COMMENT '评价结果',
  `content` text COMMENT '评价内容',
  `rate_nick` varchar(50) DEFAULT NULL COMMENT '评价昵称',
  `reply` text COMMENT '回复内容',
  UNIQUE KEY `createtime_itemid_nick_oid` (`createtime`,`itemid`,`nick`,`oid`),
  KEY `title` (`title`),
  KEY `result` (`result`),
  KEY `rate_nick` (`rate_nick`),
  KEY `role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

