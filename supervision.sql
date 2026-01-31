/*
 Navicat Premium Dump SQL

 Source Server         : 本地MYSQL
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : supervision

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 31/01/2026 18:56:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for audit_log
-- ----------------------------
DROP TABLE IF EXISTS `audit_log`;
CREATE TABLE `audit_log`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `action` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `object_id` int NULL DEFAULT NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_ip` char(39) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `detail` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `audit_log_user_id_a1b3392d_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `audit_log_user_id_a1b3392d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 118 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of audit_log
-- ----------------------------
INSERT INTO `audit_log` VALUES (1, 'create', 'crawl_task', 1, '全量爬取 - 运行中', NULL, '任务类型: 全量爬取, 地区: 全部', '2026-01-29 10:40:51.470254', NULL);
INSERT INTO `audit_log` VALUES (2, 'create', 'news', 1, '西安高新区丈八街道党工委书记杨明接受纪律审查和监察调查', NULL, '标题: 西安高新区丈八街道党工委书记杨明接受纪律审查和监察调查', '2026-01-29 10:40:51.876948', NULL);
INSERT INTO `audit_log` VALUES (3, 'create', 'news', 2, '西安市政协原副秘书长、政协办公厅原一级巡视员任立新接受纪律审查和监察调查', NULL, '标题: 西安市政协原副秘书长、政协办公厅原一级巡视员任立新接受纪律审查和监察调查', '2026-01-29 10:40:51.884984', NULL);
INSERT INTO `audit_log` VALUES (4, 'create', 'news', 3, '西安市未央区医疗保障局一级调研员弓春梅接受纪律审查和监察调查', NULL, '标题: 西安市未央区医疗保障局一级调研员弓春梅接受纪律审查和监察调查', '2026-01-29 10:40:51.888951', NULL);
INSERT INTO `audit_log` VALUES (5, 'create', 'news', 4, '莲湖区西关街道综合执法队原队长贺航被开除公职', NULL, '标题: 莲湖区西关街道综合执法队原队长贺航被开除公职', '2026-01-29 10:40:51.892515', NULL);
INSERT INTO `audit_log` VALUES (6, 'create', 'news', 5, '莲湖区土门街道综合执法队原队长朱明被开除党籍和公职', NULL, '标题: 莲湖区土门街道综合执法队原队长朱明被开除党籍和公职', '2026-01-29 10:40:51.896731', NULL);
INSERT INTO `audit_log` VALUES (7, 'create', 'news', 6, '莲湖区土门街道综合执法队原副队长张鹏被开除党籍和公职', NULL, '标题: 莲湖区土门街道综合执法队原副队长张鹏被开除党籍和公职', '2026-01-29 10:40:51.901448', NULL);
INSERT INTO `audit_log` VALUES (8, 'create', 'news', 7, '宝鸡市公共资源交易中心原主任赵峰接受纪律审查和监察调查', NULL, '标题: 宝鸡市公共资源交易中心原主任赵峰接受纪律审查和监察调查', '2026-01-29 10:40:53.288062', NULL);
INSERT INTO `audit_log` VALUES (9, 'create', 'news', 8, '原宝鸡市城乡建设规划局党组书记、局长杨锦辉接受纪律审查和监察调查', NULL, '标题: 原宝鸡市城乡建设规划局党组书记、局长杨锦辉接受纪律审查和监察调查', '2026-01-29 10:40:53.290946', NULL);
INSERT INTO `audit_log` VALUES (10, 'create', 'news', 9, '中国民航大学飞行分校（飞行技术学院）招飞办公室主任崔雪超接受纪律审查', NULL, '标题: 中国民航大学飞行分校（飞行技术学院）招飞办公室主任崔雪超接受纪律审查', '2026-01-29 10:40:53.294167', NULL);
INSERT INTO `audit_log` VALUES (11, 'create', 'news', 10, '陕西昌荣纺织有限责任公司原总会计师李光剑接受纪律审查和监察调查', NULL, '标题: 陕西昌荣纺织有限责任公司原总会计师李光剑接受纪律审查和监察调查', '2026-01-29 10:40:53.296824', NULL);
INSERT INTO `audit_log` VALUES (12, 'create', 'news', 11, '陕西昌荣纺织有限责任公司原副总经理杜剑峰接受纪律审查和监察调查', NULL, '标题: 陕西昌荣纺织有限责任公司原副总经理杜剑峰接受纪律审查和监察调查', '2026-01-29 10:40:53.300411', NULL);
INSERT INTO `audit_log` VALUES (13, 'create', 'news', 12, '宝鸡铁路技师学院原院长潘卫东严重违纪违法被开除党籍和公职', NULL, '标题: 宝鸡铁路技师学院原院长潘卫东严重违纪违法被开除党籍和公职', '2026-01-29 10:40:53.304090', NULL);
INSERT INTO `audit_log` VALUES (14, 'create', 'news', 13, '法门文化景区管委会党工委原委员、管委会原副主任李丰安严重违纪违法被开', NULL, '标题: 法门文化景区管委会党工委原委员、管委会原副主任李丰安严重违纪违法被开', '2026-01-29 10:40:53.307403', NULL);
INSERT INTO `audit_log` VALUES (15, 'create', 'news', 14, '原宝鸡市计生局党组书记、局长王喆 严重违纪违法被开除党籍、取消退休待', NULL, '标题: 原宝鸡市计生局党组书记、局长王喆 严重违纪违法被开除党籍、取消退休待', '2026-01-29 10:40:53.309722', NULL);
INSERT INTO `audit_log` VALUES (16, 'create', 'news', 15, '宝鸡市陇县中医医院原院长曹云超严重违纪违法被开除党籍和公职', NULL, '标题: 宝鸡市陇县中医医院原院长曹云超严重违纪违法被开除党籍和公职', '2026-01-29 10:40:53.313193', NULL);
INSERT INTO `audit_log` VALUES (17, 'create', 'news', 16, '宝鸡市陈仓区粮油购销公司原法定代表人、总经理吴宝田、原会计董拉让严重', NULL, '标题: 宝鸡市陈仓区粮油购销公司原法定代表人、总经理吴宝田、原会计董拉让严重', '2026-01-29 10:40:53.316839', NULL);
INSERT INTO `audit_log` VALUES (18, 'create', 'news', 17, '吴堡县政府原副县长薛永升接受监察调查', NULL, '标题: 吴堡县政府原副县长薛永升接受监察调查', '2026-01-29 10:40:53.714168', NULL);
INSERT INTO `audit_log` VALUES (19, 'create', 'news', 18, '中国中化西北橡胶塑料研究设计院有限公司原党委书记、总经理乐贵强…', NULL, '标题: 中国中化西北橡胶塑料研究设计院有限公司原党委书记、总经理乐贵强…', '2026-01-29 10:40:53.728839', NULL);
INSERT INTO `audit_log` VALUES (20, 'create', 'news', 19, '陕西中医药大学副校长缪峰接受纪律审查和监察调查', NULL, '标题: 陕西中医药大学副校长缪峰接受纪律审查和监察调查', '2026-01-29 10:40:53.739694', NULL);
INSERT INTO `audit_log` VALUES (21, 'create', 'news', 20, '陕西农业发展集团有限公司原党委书记、董事长韩霁昌接受纪律审查和…', NULL, '标题: 陕西农业发展集团有限公司原党委书记、董事长韩霁昌接受纪律审查和…', '2026-01-29 10:40:53.759765', NULL);
INSERT INTO `audit_log` VALUES (22, 'create', 'news', 21, '西安市生态环境局党委委员、西安市生态环境保护综合执法支队支队长…', NULL, '标题: 西安市生态环境局党委委员、西安市生态环境保护综合执法支队支队长…', '2026-01-29 10:40:53.781095', NULL);
INSERT INTO `audit_log` VALUES (23, 'create', 'news', 22, '陕西省广播电视局原副局长刘生胜接受纪律审查和监察调查', NULL, '标题: 陕西省广播电视局原副局长刘生胜接受纪律审查和监察调查', '2026-01-29 10:40:53.801283', NULL);
INSERT INTO `audit_log` VALUES (24, 'create', 'news', 23, '西安市人大常委会原副主任康军接受纪律审查和监察调查', NULL, '标题: 西安市人大常委会原副主任康军接受纪律审查和监察调查', '2026-01-29 10:40:53.819620', NULL);
INSERT INTO `audit_log` VALUES (25, 'create', 'news', 24, '陕西省西安市人大常委会党组书记、主任韩松接受中央纪委国家监委纪…', NULL, '标题: 陕西省西安市人大常委会党组书记、主任韩松接受中央纪委国家监委纪…', '2026-01-29 10:40:53.828656', NULL);
INSERT INTO `audit_log` VALUES (26, 'create', 'news', 25, '榆林市住房和城乡建设局原局长、二级巡视员雷亚成接受审查调查', NULL, '标题: 榆林市住房和城乡建设局原局长、二级巡视员雷亚成接受审查调查', '2026-01-29 10:40:53.831492', NULL);
INSERT INTO `audit_log` VALUES (27, 'create', 'news', 26, '陕西省工业和信息化厅原副厅长蔡苏昌接受纪律审查和监察调查', NULL, '标题: 陕西省工业和信息化厅原副厅长蔡苏昌接受纪律审查和监察调查', '2026-01-29 10:40:53.836370', NULL);
INSERT INTO `audit_log` VALUES (28, 'create', 'news', 27, '榆林市人大常委会原党组成员、副主任王效力接受纪律审查和监察调查', NULL, '标题: 榆林市人大常委会原党组成员、副主任王效力接受纪律审查和监察调查', '2026-01-29 10:40:53.840333', NULL);
INSERT INTO `audit_log` VALUES (29, 'create', 'news', 28, '青海省政协党组成员、副主席马丰胜接受中央纪委国家监委纪律审查和…', NULL, '标题: 青海省政协党组成员、副主席马丰胜接受中央纪委国家监委纪律审查和…', '2026-01-29 10:40:53.847847', NULL);
INSERT INTO `audit_log` VALUES (30, 'create', 'news', 29, '中央宣传部原副部长张建春严重违纪违法被开除党籍和公职', NULL, '标题: 中央宣传部原副部长张建春严重违纪违法被开除党籍和公职', '2026-01-29 10:40:53.852488', NULL);
INSERT INTO `audit_log` VALUES (31, 'create', 'news', 30, '合阳：组织纪检监察干部集...', NULL, '标题: 合阳：组织纪检监察干部集...', '2026-01-29 10:40:55.648178', NULL);
INSERT INTO `audit_log` VALUES (32, 'create', 'news', 31, '蒲城县纪委监委：全链条发...', NULL, '标题: 蒲城县纪委监委：全链条发...', '2026-01-29 10:40:55.650617', NULL);
INSERT INTO `audit_log` VALUES (33, 'create', 'news', 32, '我市举办新提拔干部和年轻...', NULL, '标题: 我市举办新提拔干部和年轻...', '2026-01-29 10:40:55.653505', NULL);
INSERT INTO `audit_log` VALUES (34, 'create', 'news', 33, '临渭：开展新任纪检监察领...', NULL, '标题: 临渭：开展新任纪检监察领...', '2026-01-29 10:40:55.656515', NULL);
INSERT INTO `audit_log` VALUES (35, 'create', 'news', 34, '合阳：召开全县纪检监察系...', NULL, '标题: 合阳：召开全县纪检监察系...', '2026-01-29 10:40:55.659133', NULL);
INSERT INTO `audit_log` VALUES (36, 'create', 'news', 35, '【集中整治进行时】临渭：...', NULL, '标题: 【集中整治进行时】临渭：...', '2026-01-29 10:40:55.661398', NULL);
INSERT INTO `audit_log` VALUES (37, 'create', 'news', 36, '蒲城：“五个一”上好新入...', NULL, '标题: 蒲城：“五个一”上好新入...', '2026-01-29 10:40:55.664150', NULL);
INSERT INTO `audit_log` VALUES (38, 'create', 'news', 37, '大荔县纪委监委召开2024年...', NULL, '标题: 大荔县纪委监委召开2024年...', '2026-01-29 10:40:55.666505', NULL);
INSERT INTO `audit_log` VALUES (39, 'create', 'news', 38, '富平：任前廉考为新任干部...', NULL, '标题: 富平：任前廉考为新任干部...', '2026-01-29 10:40:55.669227', NULL);
INSERT INTO `audit_log` VALUES (40, 'create', 'news', 39, '华阴市岳庙街道：“五一”...', NULL, '标题: 华阴市岳庙街道：“五一”...', '2026-01-29 10:40:55.672414', NULL);
INSERT INTO `audit_log` VALUES (41, 'create', 'news', 40, '强化对村巡察 促进解决基层...', NULL, '标题: 强化对村巡察 促进解决基层...', '2026-01-29 10:40:55.675376', NULL);
INSERT INTO `audit_log` VALUES (42, 'create', 'news', 41, '明纪释法丨严肃查处违规滥...', NULL, '标题: 明纪释法丨严肃查处违规滥...', '2026-01-29 10:40:55.678052', NULL);
INSERT INTO `audit_log` VALUES (43, 'create', 'news', 42, '中共中央印发《中国共产党...', NULL, '标题: 中共中央印发《中国共产党...', '2026-01-29 10:40:55.680495', NULL);
INSERT INTO `audit_log` VALUES (44, 'create', 'news', 43, '明纪释法丨准确认定处理侵...', NULL, '标题: 明纪释法丨准确认定处理侵...', '2026-01-29 10:40:55.683487', NULL);
INSERT INTO `audit_log` VALUES (45, 'create', 'news', 44, '以案明纪释法|党员干部收受...', NULL, '标题: 以案明纪释法|党员干部收受...', '2026-01-29 10:40:55.686496', NULL);
INSERT INTO `audit_log` VALUES (46, 'create', 'news', 45, '三堂会审 | 收受管理和服务...', NULL, '标题: 三堂会审 | 收受管理和服务...', '2026-01-29 10:40:55.689730', NULL);
INSERT INTO `audit_log` VALUES (47, 'create', 'news', 46, '理论视野丨以廉洁家风 涵养...', NULL, '标题: 理论视野丨以廉洁家风 涵养...', '2026-01-29 10:40:55.692406', NULL);
INSERT INTO `audit_log` VALUES (48, 'create', 'news', 47, '渭南高新区：严守礼尚往来...', NULL, '标题: 渭南高新区：严守礼尚往来...', '2026-01-29 10:40:55.694770', NULL);
INSERT INTO `audit_log` VALUES (49, 'create', 'news', 48, '渭南市住房和城乡建设局原党组书记、局长姬智武接受纪律...', NULL, '标题: 渭南市住房和城乡建设局原党组书记、局长姬智武接受纪律...', '2026-01-29 10:40:55.696999', NULL);
INSERT INTO `audit_log` VALUES (50, 'create', 'news', 49, '华阴市太华村华峰片区二组原组长杨新虎被移送检察机关审...', NULL, '标题: 华阴市太华村华峰片区二组原组长杨新虎被移送检察机关审...', '2026-01-29 10:40:55.700326', NULL);
INSERT INTO `audit_log` VALUES (51, 'create', 'news', 50, '中国通用技术集团下属中国轻工业品进出口集团有限公司原...', NULL, '标题: 中国通用技术集团下属中国轻工业品进出口集团有限公司原...', '2026-01-29 10:40:55.702845', NULL);
INSERT INTO `audit_log` VALUES (52, 'create', 'news', 51, '渭南市临渭区人民法院审判委员会委员李亚红接受审查调查', NULL, '标题: 渭南市临渭区人民法院审判委员会委员李亚红接受审查调查', '2026-01-29 10:40:55.705113', NULL);
INSERT INTO `audit_log` VALUES (53, 'create', 'news', 52, '韩城市人民法院审判监督庭原庭长贾克俭接受审查调查', NULL, '标题: 韩城市人民法院审判监督庭原庭长贾克俭接受审查调查', '2026-01-29 10:40:55.708000', NULL);
INSERT INTO `audit_log` VALUES (54, 'create', 'news', 53, '渭南市纪委监委通报4起违反中央八项规定精神问题典型案例', NULL, '标题: 渭南市纪委监委通报4起违反中央八项规定精神问题典型案例', '2026-01-29 10:40:55.710769', NULL);
INSERT INTO `audit_log` VALUES (55, 'create', 'news', 54, '渭南市纪委监委通报10起酒驾醉驾典型案例', NULL, '标题: 渭南市纪委监委通报10起酒驾醉驾典型案例', '2026-01-29 10:40:55.713100', NULL);
INSERT INTO `audit_log` VALUES (56, 'create', 'news', 55, '渭南市纪委监委通报8起酒驾醉驾典型案例', NULL, '标题: 渭南市纪委监委通报8起酒驾醉驾典型案例', '2026-01-29 10:40:55.716544', NULL);
INSERT INTO `audit_log` VALUES (57, 'create', 'news', 56, '渭南市纪委监委通报3起群众身边腐败和作风问题典型案例', NULL, '标题: 渭南市纪委监委通报3起群众身边腐败和作风问题典型案例', '2026-01-29 10:40:55.719621', NULL);
INSERT INTO `audit_log` VALUES (58, 'create', 'news', 57, '渭南市纪委监委通报2起违规发展党员问题典型案例', NULL, '标题: 渭南市纪委监委通报2起违规发展党员问题典型案例', '2026-01-29 10:40:55.722675', NULL);
INSERT INTO `audit_log` VALUES (59, 'create', 'news', 58, '中国石油长庆油田公司技术检测中心原主任李国庆接受纪律审查和监察调查', NULL, '标题: 中国石油长庆油田公司技术检测中心原主任李国庆接受纪律审查和监察调查', '2026-01-29 10:40:56.402758', NULL);
INSERT INTO `audit_log` VALUES (60, 'create', 'news', 59, '中国矿业大学（北京）原党委常委、副校长范中启接受审查调查', NULL, '标题: 中国矿业大学（北京）原党委常委、副校长范中启接受审查调查', '2026-01-29 10:40:56.406545', NULL);
INSERT INTO `audit_log` VALUES (61, 'create', 'news', 60, '延安市原土地统征管理办公室主任张剑君接受纪律审查和监察调查', NULL, '标题: 延安市原土地统征管理办公室主任张剑君接受纪律审查和监察调查', '2026-01-29 10:40:56.411290', NULL);
INSERT INTO `audit_log` VALUES (62, 'create', 'news', 61, '延安市中级人民法院四级高级法官赵伟接受纪律审查和监察调查', NULL, '标题: 延安市中级人民法院四级高级法官赵伟接受纪律审查和监察调查', '2026-01-29 10:40:56.419791', NULL);
INSERT INTO `audit_log` VALUES (63, 'create', 'news', 62, '延安水务环保集团自来水有限公司原总经理李中华接受纪律审查和监察调查', NULL, '标题: 延安水务环保集团自来水有限公司原总经理李中华接受纪律审查和监察调查', '2026-01-29 10:40:56.439053', NULL);
INSERT INTO `audit_log` VALUES (64, 'create', 'news', 63, '延安市甘泉县人民法院原党组成员、执行局局长杨金成接受纪律审查和监察调查', NULL, '标题: 延安市甘泉县人民法院原党组成员、执行局局长杨金成接受纪律审查和监察调查', '2026-01-29 10:40:56.461451', NULL);
INSERT INTO `audit_log` VALUES (65, 'create', 'news', 64, '延安市甘泉县财政局原收费中心主任谢嘉平接受纪律审查和监察调查', NULL, '标题: 延安市甘泉县财政局原收费中心主任谢嘉平接受纪律审查和监察调查', '2026-01-29 10:40:56.485437', NULL);
INSERT INTO `audit_log` VALUES (66, 'create', 'news', 65, '延安市黄陵中学原校长蔡永峰接受纪律审查和监察调查', NULL, '标题: 延安市黄陵中学原校长蔡永峰接受纪律审查和监察调查', '2026-01-29 10:40:56.496872', NULL);
INSERT INTO `audit_log` VALUES (67, 'create', 'news', 66, '延安市人力资源和社会保障局原党组成员、副局长党鹏严重违纪违法被开除党籍', NULL, '标题: 延安市人力资源和社会保障局原党组成员、副局长党鹏严重违纪违法被开除党籍', '2026-01-29 10:40:56.511991', NULL);
INSERT INTO `audit_log` VALUES (68, 'create', 'news', 67, '延安市子长市粮油购销有限公司原经理李胜利接受纪律审查和监察调查', NULL, '标题: 延安市子长市粮油购销有限公司原经理李胜利接受纪律审查和监察调查', '2026-01-29 10:40:56.529599', NULL);
INSERT INTO `audit_log` VALUES (69, 'create', 'news', 68, '延安市安塞区沿河湾镇财政所原所长张文伟接受纪律审查和监察调查', NULL, '标题: 延安市安塞区沿河湾镇财政所原所长张文伟接受纪律审查和监察调查', '2026-01-29 10:40:56.534099', NULL);
INSERT INTO `audit_log` VALUES (70, 'create', 'news', 69, '延安市城市管理监督指挥中心原副主任杜月飞接受纪律审查和监察调查', NULL, '标题: 延安市城市管理监督指挥中心原副主任杜月飞接受纪律审查和监察调查', '2026-01-29 10:40:56.538630', NULL);
INSERT INTO `audit_log` VALUES (71, 'create', 'news', 70, '延安市人力资源和社会保障局原党组成员、副局长党鹏接受纪律审查和监察调查', NULL, '标题: 延安市人力资源和社会保障局原党组成员、副局长党鹏接受纪律审查和监察调查', '2026-01-29 10:40:56.542921', NULL);
INSERT INTO `audit_log` VALUES (72, 'create', 'news', 71, '甘泉县环境卫生和园林绿化管理站主任曹新接受纪律审查和监察调查', NULL, '标题: 甘泉县环境卫生和园林绿化管理站主任曹新接受纪律审查和监察调查', '2026-01-29 10:40:56.547024', NULL);
INSERT INTO `audit_log` VALUES (73, 'create', 'news', 72, '榆林市生态环境局子洲分局局长贺腾飞接受审查调查', NULL, '标题: 榆林市生态环境局子洲分局局长贺腾飞接受审查调查', '2026-01-29 10:40:56.923677', NULL);
INSERT INTO `audit_log` VALUES (74, 'create', 'news', 73, '吴堡县政府原副县长薛永升接受监察调查', NULL, '标题: 吴堡县政府原副县长薛永升接受监察调查', '2026-01-29 10:40:56.929045', NULL);
INSERT INTO `audit_log` VALUES (75, 'create', 'news', 74, '榆林市第一医院原院长冯丙东接受审查调查', NULL, '标题: 榆林市第一医院原院长冯丙东接受审查调查', '2026-01-29 10:40:56.936942', NULL);
INSERT INTO `audit_log` VALUES (76, 'create', 'news', 75, '定边县民政局原局长马保贵接受审查调查', NULL, '标题: 定边县民政局原局长马保贵接受审查调查', '2026-01-29 10:40:56.940057', NULL);
INSERT INTO `audit_log` VALUES (77, 'create', 'news', 76, '神木市公安局尔林兔派出所所长杨金良接受审查调查', NULL, '标题: 神木市公安局尔林兔派出所所长杨金良接受审查调查', '2026-01-29 10:40:56.943801', NULL);
INSERT INTO `audit_log` VALUES (78, 'create', 'news', 77, '榆林市住房和城乡建设局原局长、二级巡视员雷亚成接受审查调查', NULL, '标题: 榆林市住房和城乡建设局原局长、二级巡视员雷亚成接受审查调查', '2026-01-29 10:40:56.947504', NULL);
INSERT INTO `audit_log` VALUES (79, 'create', 'news', 78, '榆林市财政局党组成员、四级调研员张渝林接受审查调查', NULL, '标题: 榆林市财政局党组成员、四级调研员张渝林接受审查调查', '2026-01-29 10:40:56.950833', NULL);
INSERT INTO `audit_log` VALUES (80, 'create', 'news', 79, '神木市档案局原局长闫晓庆接受审查调查', NULL, '标题: 神木市档案局原局长闫晓庆接受审查调查', '2026-01-29 10:40:56.953801', NULL);
INSERT INTO `audit_log` VALUES (81, 'create', 'news', 80, '佳县人民医院原党支部书记、院长李红卫接受审查调查', NULL, '标题: 佳县人民医院原党支部书记、院长李红卫接受审查调查', '2026-01-29 10:40:56.957557', NULL);
INSERT INTO `audit_log` VALUES (82, 'create', 'news', 81, '绥德县四十里铺镇崔家圪崂村党支部书记、村委会主任郝建军接...', NULL, '标题: 绥德县四十里铺镇崔家圪崂村党支部书记、村委会主任郝建军接...', '2026-01-29 10:40:56.960965', NULL);
INSERT INTO `audit_log` VALUES (83, 'create', 'news', 82, '中信银行呼和浩特分行原党委委员、行长助理王志忠接受审查调查', NULL, '标题: 中信银行呼和浩特分行原党委委员、行长助理王志忠接受审查调查', '2026-01-29 10:40:57.345491', NULL);
INSERT INTO `audit_log` VALUES (84, 'create', 'news', 83, '略阳县卫健局原党组书记、局长、三级调研员胡荣昌接受纪律审查和监察调查', NULL, '标题: 略阳县卫健局原党组书记、局长、三级调研员胡荣昌接受纪律审查和监察调查', '2026-01-29 10:40:57.349438', NULL);
INSERT INTO `audit_log` VALUES (85, 'create', 'news', 84, '汉中市南郑区政协党组原副书记、副主席、红庙镇党委原书记朱以荣被开除党籍和公职', NULL, '标题: 汉中市南郑区政协党组原副书记、副主席、红庙镇党委原书记朱以荣被开除党籍和公职', '2026-01-29 10:40:57.353112', NULL);
INSERT INTO `audit_log` VALUES (86, 'create', 'news', 85, '陕西煤业化工集团有限责任公司原副总经理张丹力被开除党籍、取消退休待遇', NULL, '标题: 陕西煤业化工集团有限责任公司原副总经理张丹力被开除党籍、取消退休待遇', '2026-01-29 10:40:57.356185', NULL);
INSERT INTO `audit_log` VALUES (87, 'create', 'news', 86, '汉中市公安局经济开发区分局党委委员、副局长白靖接受纪律审查和监察调查', NULL, '标题: 汉中市公安局经济开发区分局党委委员、副局长白靖接受纪律审查和监察调查', '2026-01-29 10:40:57.359972', NULL);
INSERT INTO `audit_log` VALUES (88, 'create', 'news', 87, '汉中市南郑区政协党组副书记、副主席、红庙镇党委书记朱以荣接受审查调查', NULL, '标题: 汉中市南郑区政协党组副书记、副主席、红庙镇党委书记朱以荣接受审查调查', '2026-01-29 10:40:57.363425', NULL);
INSERT INTO `audit_log` VALUES (89, 'create', 'news', 88, '汉中市公安局原党委委员、副局长王雨团被开除党籍', NULL, '标题: 汉中市公安局原党委委员、副局长王雨团被开除党籍', '2026-01-29 10:40:57.366259', NULL);
INSERT INTO `audit_log` VALUES (90, 'create', 'news', 89, '西安市政公用建设投资集团有限公司原党委书记、董事长毛浓成接受审查调查', NULL, '标题: 西安市政公用建设投资集团有限公司原党委书记、董事长毛浓成接受审查调查', '2026-01-29 10:40:57.370003', NULL);
INSERT INTO `audit_log` VALUES (91, 'create', 'news', 90, '汉中市宝汉高速公路项目协调办公室专职副主任韩文玉接受审查调查', NULL, '标题: 汉中市宝汉高速公路项目协调办公室专职副主任韩文玉接受审查调查', '2026-01-29 10:40:57.373856', NULL);
INSERT INTO `audit_log` VALUES (92, 'create', 'news', 91, '青海省副省长、海西蒙古族藏族自治州委书记、柴达木循环经济试验区党工委书记文国...', NULL, '标题: 青海省副省长、海西蒙古族藏族自治州委书记、柴达木循环经济试验区党工委书记文国...', '2026-01-29 10:40:57.377557', NULL);
INSERT INTO `audit_log` VALUES (93, 'create', 'news', 92, '咸阳市住房公积金管理中心党组书记、主任李晓强接受审查调查', NULL, '标题: 咸阳市住房公积金管理中心党组书记、主任李晓强接受审查调查', '2026-01-29 10:40:57.379767', NULL);
INSERT INTO `audit_log` VALUES (94, 'create', 'news', 93, '公安部党委委员、副部长孙力军接受中央纪委国家监委审查调查', NULL, '标题: 公安部党委委员、副部长孙力军接受中央纪委国家监委审查调查', '2026-01-29 10:40:57.382682', NULL);
INSERT INTO `audit_log` VALUES (95, 'create', 'news', 94, '西乡县委副书记、县长李耕接受纪律审查和监察调查', NULL, '标题: 西乡县委副书记、县长李耕接受纪律审查和监察调查', '2026-01-29 10:40:57.386458', NULL);
INSERT INTO `audit_log` VALUES (96, 'create', 'news', 95, '勉县县委常委、县政府副县长、党组副书记柳必成接受纪律审查和监察调查', NULL, '标题: 勉县县委常委、县政府副县长、党组副书记柳必成接受纪律审查和监察调查', '2026-01-29 10:40:57.390078', NULL);
INSERT INTO `audit_log` VALUES (97, 'create', 'news', 96, '西乡县扶贫开发办公室主任全子强接受纪律审查和监察调查', NULL, '标题: 西乡县扶贫开发办公室主任全子强接受纪律审查和监察调查', '2026-01-29 10:40:57.393942', NULL);
INSERT INTO `audit_log` VALUES (98, 'create', 'news', 97, '西乡县交通运输局局长张毅接受纪律审查和监察调查', NULL, '标题: 西乡县交通运输局局长张毅接受纪律审查和监察调查', '2026-01-29 10:40:57.397261', NULL);
INSERT INTO `audit_log` VALUES (99, 'create', 'news', 98, '西乡县河道堤防管理站副站长余跃宏接受监察调查', NULL, '标题: 西乡县河道堤防管理站副站长余跃宏接受监察调查', '2026-01-29 10:40:57.399947', NULL);
INSERT INTO `audit_log` VALUES (100, 'create', 'news', 99, '汉中市委常委秘书长统战部长牟晓非接受纪律审查和监察调查', NULL, '标题: 汉中市委常委秘书长统战部长牟晓非接受纪律审查和监察调查', '2026-01-29 10:40:57.404353', NULL);
INSERT INTO `audit_log` VALUES (101, 'create', 'news', 100, '汉中市政协秘书长卢兴成等3名处级干部接受纪律审查和监察调查', NULL, '标题: 汉中市政协秘书长卢兴成等3名处级干部接受纪律审查和监察调查', '2026-01-29 10:40:57.408308', NULL);
INSERT INTO `audit_log` VALUES (102, 'create', 'news', 101, '汉中市政协主席王隆庆接受纪律审查和监察调查', NULL, '标题: 汉中市政协主席王隆庆接受纪律审查和监察调查', '2026-01-29 10:40:57.411147', NULL);
INSERT INTO `audit_log` VALUES (103, 'create', 'news', 102, '安康市恒口示范区生态环境局局长王敦贵接受审查调查', NULL, '标题: 安康市恒口示范区生态环境局局长王敦贵接受审查调查', '2026-01-29 10:40:57.809549', NULL);
INSERT INTO `audit_log` VALUES (104, 'create', 'news', 103, '宁陕县人大常委会原副主任黄国庆接受审查调查', NULL, '标题: 宁陕县人大常委会原副主任黄国庆接受审查调查', '2026-01-29 10:40:57.813253', NULL);
INSERT INTO `audit_log` VALUES (105, 'create', 'news', 104, '旬阳市卫生健康局三级调研员李瑞清接受纪律审查和...', NULL, '标题: 旬阳市卫生健康局三级调研员李瑞清接受纪律审查和...', '2026-01-29 10:40:57.817421', NULL);
INSERT INTO `audit_log` VALUES (106, 'create', 'news', 105, '紫阳县水利局原党委书记、局长曹仲之接受纪律审查...', NULL, '标题: 紫阳县水利局原党委书记、局长曹仲之接受纪律审查...', '2026-01-29 10:40:57.820195', NULL);
INSERT INTO `audit_log` VALUES (107, 'create', 'news', 106, '石泉县民政局党组书记、局长刘军接受纪律审查和监...', NULL, '标题: 石泉县民政局党组书记、局长刘军接受纪律审查和监...', '2026-01-29 10:40:57.824029', NULL);
INSERT INTO `audit_log` VALUES (108, 'create', 'news', 107, '白河县林业局原党委书记、局长阮家顺接受纪律审查...', NULL, '标题: 白河县林业局原党委书记、局长阮家顺接受纪律审查...', '2026-01-29 10:40:57.827620', NULL);
INSERT INTO `audit_log` VALUES (109, 'create', 'news', 108, '镇坪县工商业联合会主席张春平接受监察调查', NULL, '标题: 镇坪县工商业联合会主席张春平接受监察调查', '2026-01-29 10:40:57.830228', NULL);
INSERT INTO `audit_log` VALUES (110, 'create', 'news', 109, '宁陕县教育体育和科技局原党委书记、局长   陈衍子...', NULL, '标题: 宁陕县教育体育和科技局原党委书记、局长   陈衍子...', '2026-01-29 10:40:57.834174', NULL);
INSERT INTO `audit_log` VALUES (111, 'create', 'news', 110, '安康市文化和旅游广电局原党组书记、局长杨海波受...', NULL, '标题: 安康市文化和旅游广电局原党组书记、局长杨海波受...', '2026-01-29 10:40:57.837024', NULL);
INSERT INTO `audit_log` VALUES (112, 'create', 'news', 111, '原安康市文化产业发展中心副主任、市演艺影视公司...', NULL, '标题: 原安康市文化产业发展中心副主任、市演艺影视公司...', '2026-01-29 10:40:57.840605', NULL);
INSERT INTO `audit_log` VALUES (113, 'create', 'news', 112, '安康市公安局汉滨分局交通管理大队江北交警中队原...', NULL, '标题: 安康市公安局汉滨分局交通管理大队江北交警中队原...', '2026-01-29 10:40:57.843443', NULL);
INSERT INTO `audit_log` VALUES (114, 'create', 'news', 113, '镇坪县人大常委会党组成员、副主任韦树辉严重违纪...', NULL, '标题: 镇坪县人大常委会党组成员、副主任韦树辉严重违纪...', '2026-01-29 10:40:57.846494', NULL);
INSERT INTO `audit_log` VALUES (115, 'create', 'news', 114, '镇坪县财政局政府采购管理股股长程斌严重违纪违法...', NULL, '标题: 镇坪县财政局政府采购管理股股长程斌严重违纪违法...', '2026-01-29 10:40:57.848696', NULL);
INSERT INTO `audit_log` VALUES (116, 'create', 'news', 115, '市中心医院原院长、党委副书记王永堂因违纪受到党...', NULL, '标题: 市中心医院原院长、党委副书记王永堂因违纪受到党...', '2026-01-29 10:40:57.851613', NULL);
INSERT INTO `audit_log` VALUES (117, 'crawl', 'crawl_task', 1, '全量爬取 - 成功', NULL, '状态: 成功, 爬取: 115条, 新增: 115条', '2026-01-29 10:40:59.623445', NULL);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 65 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add 地区', 7, 'add_region');
INSERT INTO `auth_permission` VALUES (26, 'Can change 地区', 7, 'change_region');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 地区', 7, 'delete_region');
INSERT INTO `auth_permission` VALUES (28, 'Can view 地区', 7, 'view_region');
INSERT INTO `auth_permission` VALUES (29, 'Can add 标签分类', 8, 'add_tagcategory');
INSERT INTO `auth_permission` VALUES (30, 'Can change 标签分类', 8, 'change_tagcategory');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 标签分类', 8, 'delete_tagcategory');
INSERT INTO `auth_permission` VALUES (32, 'Can view 标签分类', 8, 'view_tagcategory');
INSERT INTO `auth_permission` VALUES (33, 'Can add 标签', 9, 'add_tag');
INSERT INTO `auth_permission` VALUES (34, 'Can change 标签', 9, 'change_tag');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 标签', 9, 'delete_tag');
INSERT INTO `auth_permission` VALUES (36, 'Can view 标签', 9, 'view_tag');
INSERT INTO `auth_permission` VALUES (37, 'Can add 新闻', 10, 'add_news');
INSERT INTO `auth_permission` VALUES (38, 'Can change 新闻', 10, 'change_news');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 新闻', 10, 'delete_news');
INSERT INTO `auth_permission` VALUES (40, 'Can view 新闻', 10, 'view_news');
INSERT INTO `auth_permission` VALUES (41, 'Can add 爬取日志', 11, 'add_crawllog');
INSERT INTO `auth_permission` VALUES (42, 'Can change 爬取日志', 11, 'change_crawllog');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 爬取日志', 11, 'delete_crawllog');
INSERT INTO `auth_permission` VALUES (44, 'Can view 爬取日志', 11, 'view_crawllog');
INSERT INTO `auth_permission` VALUES (45, 'Can add 爬虫任务', 12, 'add_crawltask');
INSERT INTO `auth_permission` VALUES (46, 'Can change 爬虫任务', 12, 'change_crawltask');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 爬虫任务', 12, 'delete_crawltask');
INSERT INTO `auth_permission` VALUES (48, 'Can view 爬虫任务', 12, 'view_crawltask');
INSERT INTO `auth_permission` VALUES (49, 'Can add 审计日志', 13, 'add_auditlog');
INSERT INTO `auth_permission` VALUES (50, 'Can change 审计日志', 13, 'change_auditlog');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 审计日志', 13, 'delete_auditlog');
INSERT INTO `auth_permission` VALUES (52, 'Can view 审计日志', 13, 'view_auditlog');
INSERT INTO `auth_permission` VALUES (53, 'Can add 调度执行日志', 14, 'add_crawlschedulelog');
INSERT INTO `auth_permission` VALUES (54, 'Can change 调度执行日志', 14, 'change_crawlschedulelog');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 调度执行日志', 14, 'delete_crawlschedulelog');
INSERT INTO `auth_permission` VALUES (56, 'Can view 调度执行日志', 14, 'view_crawlschedulelog');
INSERT INTO `auth_permission` VALUES (57, 'Can add 爬虫任务配置', 15, 'add_crawlconfig');
INSERT INTO `auth_permission` VALUES (58, 'Can change 爬虫任务配置', 15, 'change_crawlconfig');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 爬虫任务配置', 15, 'delete_crawlconfig');
INSERT INTO `auth_permission` VALUES (60, 'Can view 爬虫任务配置', 15, 'view_crawlconfig');
INSERT INTO `auth_permission` VALUES (61, 'Can add 监督事项清单', 16, 'add_supervisionitem');
INSERT INTO `auth_permission` VALUES (62, 'Can change 监督事项清单', 16, 'change_supervisionitem');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 监督事项清单', 16, 'delete_supervisionitem');
INSERT INTO `auth_permission` VALUES (64, 'Can view 监督事项清单', 16, 'view_supervisionitem');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$600000$hFr62Jvu7rDY6u8eYtly3P$vqGpsfUB/cAiYUzM4da2IO99VqPze/oYwVVbsl0e7E8=', NULL, 1, 'ynchen', '', '', '1911779729@qq.com', 1, 1, '2026-01-28 04:25:29.869403');
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$600000$JTD5Zav9ZJPxFrOFBXS7vJ$32t8iPdo3UKSbSs2oQa3lwDhpQUWAWNHnnfKHe263YU=', '2026-01-31 10:49:04.656571', 1, 'hq', '', '', '1911779729@qq.com', 1, 1, '2026-01-28 04:28:50.203754');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for crawl_config
-- ----------------------------
DROP TABLE IF EXISTS `crawl_config`;
CREATE TABLE `crawl_config`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `trigger_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `interval_hours` int NOT NULL,
  `cron_hour` int NOT NULL,
  `cron_minute` int NOT NULL,
  `is_enabled` tinyint(1) NOT NULL,
  `max_instances` int NOT NULL,
  `crawl_all_regions` tinyint(1) NOT NULL,
  `region_codes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `crawl_config_created_by_id_3d0ab49a_fk_auth_user_id`(`created_by_id` ASC) USING BTREE,
  CONSTRAINT `crawl_config_created_by_id_3d0ab49a_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of crawl_config
-- ----------------------------

-- ----------------------------
-- Table structure for crawl_log
-- ----------------------------
DROP TABLE IF EXISTS `crawl_log`;
CREATE TABLE `crawl_log`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `region_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_crawled` int NOT NULL,
  `new_count` int NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `error_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crawl_time` datetime(6) NOT NULL,
  `duration` double NOT NULL,
  `region_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `crawl_log_region_id_276b4004_fk_region_id`(`region_id` ASC) USING BTREE,
  CONSTRAINT `crawl_log_region_id_276b4004_fk_region_id` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of crawl_log
-- ----------------------------
INSERT INTO `crawl_log` VALUES (1, '西安市', 6, 6, 'success', '', '2026-01-29 10:40:51.906405', 0.43140530586242676, 1);
INSERT INTO `crawl_log` VALUES (2, '宝鸡市', 10, 10, 'success', '', '2026-01-29 10:40:53.321356', 1.4108121395111084, 2);
INSERT INTO `crawl_log` VALUES (3, '咸阳市', 13, 13, 'success', '', '2026-01-29 10:40:53.857602', 0.5326342582702637, 3);
INSERT INTO `crawl_log` VALUES (4, '铜川市', 0, 0, 'error', 'HTTP 404', '2026-01-29 10:40:55.262539', 1.3996317386627197, 4);
INSERT INTO `crawl_log` VALUES (5, '渭南市', 28, 28, 'success', '', '2026-01-29 10:40:55.727081', 0.4597806930541992, 5);
INSERT INTO `crawl_log` VALUES (6, '延安市', 14, 14, 'success', '', '2026-01-29 10:40:56.554501', 0.8240857124328613, 6);
INSERT INTO `crawl_log` VALUES (7, '榆林市', 10, 10, 'success', '', '2026-01-29 10:40:56.964359', 0.4056355953216553, 7);
INSERT INTO `crawl_log` VALUES (8, '汉中市', 20, 20, 'success', '', '2026-01-29 10:40:57.415692', 0.4477086067199707, 8);
INSERT INTO `crawl_log` VALUES (9, '安康市', 14, 14, 'success', '', '2026-01-29 10:40:57.856465', 0.43738412857055664, 9);
INSERT INTO `crawl_log` VALUES (10, '商洛市', 0, 0, 'error', 'HTTP 404', '2026-01-29 10:40:59.217316', 1.3564400672912598, 10);
INSERT INTO `crawl_log` VALUES (11, '杨凌示范区', 0, 0, 'error', 'HTTP 404', '2026-01-29 10:40:59.611835', 0.3843855857849121, 11);

-- ----------------------------
-- Table structure for crawl_schedule_log
-- ----------------------------
DROP TABLE IF EXISTS `crawl_schedule_log`;
CREATE TABLE `crawl_schedule_log`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `trigger_time` datetime(6) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_crawled` int NOT NULL,
  `new_count` int NOT NULL,
  `error_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration` double NOT NULL,
  `config_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `crawl_schedule_log_config_id_de5f3a22_fk_crawl_config_id`(`config_id` ASC) USING BTREE,
  CONSTRAINT `crawl_schedule_log_config_id_de5f3a22_fk_crawl_config_id` FOREIGN KEY (`config_id`) REFERENCES `crawl_config` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of crawl_schedule_log
-- ----------------------------

-- ----------------------------
-- Table structure for crawl_task
-- ----------------------------
DROP TABLE IF EXISTS `crawl_task`;
CREATE TABLE `crawl_task`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `region_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_crawled` int NOT NULL,
  `new_count` int NOT NULL,
  `error_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `started_at` datetime(6) NULL DEFAULT NULL,
  `finished_at` datetime(6) NULL DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int NULL DEFAULT NULL,
  `region_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `crawl_task_created_by_id_29f758fd_fk_auth_user_id`(`created_by_id` ASC) USING BTREE,
  INDEX `crawl_task_region_id_0eb21d3c_fk_region_id`(`region_id` ASC) USING BTREE,
  CONSTRAINT `crawl_task_created_by_id_29f758fd_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `crawl_task_region_id_0eb21d3c_fk_region_id` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of crawl_task
-- ----------------------------
INSERT INTO `crawl_task` VALUES (1, 'all', '', 'success', 115, 115, '', '2026-01-29 10:40:51.398608', '2026-01-29 10:40:59.618965', '2026-01-29 10:40:51.453558', NULL, NULL);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (15, 'crawler', 'crawlconfig');
INSERT INTO `django_content_type` VALUES (14, 'crawler', 'crawlschedulelog');
INSERT INTO `django_content_type` VALUES (13, 'news', 'auditlog');
INSERT INTO `django_content_type` VALUES (11, 'news', 'crawllog');
INSERT INTO `django_content_type` VALUES (12, 'news', 'crawltask');
INSERT INTO `django_content_type` VALUES (10, 'news', 'news');
INSERT INTO `django_content_type` VALUES (7, 'news', 'region');
INSERT INTO `django_content_type` VALUES (16, 'news', 'supervisionitem');
INSERT INTO `django_content_type` VALUES (9, 'news', 'tag');
INSERT INTO `django_content_type` VALUES (8, 'news', 'tagcategory');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2026-01-28 04:14:44.285356');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2026-01-28 04:14:45.008251');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2026-01-28 04:14:45.172341');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2026-01-28 04:14:45.178405');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-28 04:14:45.184987');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2026-01-28 04:14:45.456118');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2026-01-28 04:14:45.542755');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2026-01-28 04:14:45.563479');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2026-01-28 04:14:45.572882');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2026-01-28 04:14:45.638132');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2026-01-28 04:14:45.644050');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2026-01-28 04:14:45.650627');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2026-01-28 04:14:45.726874');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2026-01-28 04:14:45.797834');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2026-01-28 04:14:45.814289');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2026-01-28 04:14:45.826318');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2026-01-28 04:14:45.909060');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2026-01-28 04:14:45.949464');
INSERT INTO `django_migrations` VALUES (19, 'news', '0001_initial', '2026-01-28 04:23:52.269582');
INSERT INTO `django_migrations` VALUES (20, 'news', '0002_crawltask_auditlog', '2026-01-28 10:32:35.738662');
INSERT INTO `django_migrations` VALUES (21, 'crawler', '0001_initial', '2026-01-29 11:07:25.915324');
INSERT INTO `django_migrations` VALUES (22, 'news', '0003_news_corrected_at_news_corrected_by_and_more', '2026-01-29 12:03:53.299029');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('ey5lsyd72i7148miavy33rfzx3u09vaj', '.eJxVjDkOwjAUBe_iGln58RpK-pwh-hs4gGIpS4W4O0RKAe2bmfcyA25rGbZF52EUczatOf1uhPzQaQdyx-lWLddpnUeyu2IPuti-ij4vh_t3UHAp3zpozNAE9pBjpJauxBAan7DLQIhNCi6gbzP5LgmwsFPIwXVRyEdQNe8PyN03bA:1vm8XI:yzdW3Fq61GLxCFCF05rMLcawDrbogFXsi8bnyZL6Lqw', '2026-02-14 10:49:04.665512');
INSERT INTO `django_session` VALUES ('zhrn3aqin1z39dbpx3fd89bkf9r16ku5', '.eJxVjDkOwjAUBe_iGln58RpK-pwh-hs4gGIpS4W4O0RKAe2bmfcyA25rGbZF52EUczatOf1uhPzQaQdyx-lWLddpnUeyu2IPuti-ij4vh_t3UHAp3zpozNAE9pBjpJauxBAan7DLQIhNCi6gbzP5LgmwsFPIwXVRyEdQNe8PyN03bA:1vkxB4:YxF7_JSN3JfTKBNiDGq6bhkEe1C0IlZsM6pcBR_joUA', '2026-02-11 04:29:14.541606');

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `summary` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NULL DEFAULT NULL,
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `region_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `menu` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `submenu` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tag_names` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crawl_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `view_count` int NOT NULL,
  `region_id` bigint NULL DEFAULT NULL,
  `corrected_at` datetime(6) NULL DEFAULT NULL,
  `corrected_by_id` int NULL DEFAULT NULL,
  `correction_reason` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_manual_corrected` tinyint(1) NOT NULL,
  `manual_tag_names` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `url`(`url` ASC) USING BTREE,
  INDEX `news_date_0a9db5_idx`(`date` ASC) USING BTREE,
  INDEX `news_region__3000f1_idx`(`region_id` ASC) USING BTREE,
  INDEX `news_url_306ab1_idx`(`url` ASC) USING BTREE,
  INDEX `news_corrected_by_id_fb904311_fk_auth_user_id`(`corrected_by_id` ASC) USING BTREE,
  CONSTRAINT `news_region_id_b418dd9e_fk_region_id` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `news_corrected_by_id_fb904311_fk_auth_user_id` FOREIGN KEY (`corrected_by_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 116 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of news
-- ----------------------------
INSERT INTO `news` VALUES (1, '西安高新区丈八街道党工委书记杨明接受纪律审查和监察调查', '', '', '2026-01-23', 'https://xian.qinfeng.gov.cn/info/1300/42877.htm', '清风网', '西安市', '首页', '', '执纪审查', '2026-01-29 10:40:51.876142', '2026-01-29 10:40:51.876156', 'published', 0, 1, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (2, '西安市政协原副秘书长、政协办公厅原一级巡视员任立新接受纪律审查和监察调查', '', '', '2026-01-12', 'https://xian.qinfeng.gov.cn/info/1300/42668.htm', '清风网', '西安市', '首页', '', '执纪审查', '2026-01-29 10:40:51.884471', '2026-01-29 10:40:51.884486', 'published', 0, 1, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (3, '西安市未央区医疗保障局一级调研员弓春梅接受纪律审查和监察调查', '', '', '2025-11-17', 'https://xian.qinfeng.gov.cn/info/1300/42151.htm', '清风网', '西安市', '首页', '', '教育医疗,执纪审查', '2026-01-29 10:40:51.888522', '2026-01-29 10:40:51.888534', 'published', 0, 1, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (4, '莲湖区西关街道综合执法队原队长贺航被开除公职', '', '', '2023-12-07', 'https://xian.qinfeng.gov.cn/info/1301/33378.htm', '清风网', '西安市', '首页', '', '政务处分', '2026-01-29 10:40:51.892139', '2026-01-29 10:40:51.892149', 'published', 0, 1, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (5, '莲湖区土门街道综合执法队原队长朱明被开除党籍和公职', '', '', '2023-12-07', 'https://xian.qinfeng.gov.cn/info/1301/33379.htm', '清风网', '西安市', '首页', '', '党纪处分', '2026-01-29 10:40:51.896048', '2026-01-29 10:40:51.896059', 'published', 0, 1, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (6, '莲湖区土门街道综合执法队原副队长张鹏被开除党籍和公职', '', '', '2023-12-07', 'https://xian.qinfeng.gov.cn/info/1301/33380.htm', '清风网', '西安市', '首页', '', '党纪处分', '2026-01-29 10:40:51.900914', '2026-01-29 10:40:51.900930', 'published', 0, 1, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (7, '宝鸡市公共资源交易中心原主任赵峰接受纪律审查和监察调查', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1276/28547.htm', '清风网', '宝鸡市', '首页', '', '执纪审查', '2026-01-29 10:40:53.287597', '2026-01-29 10:40:53.287611', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (8, '原宝鸡市城乡建设规划局党组书记、局长杨锦辉接受纪律审查和监察调查', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1276/26873.htm', '清风网', '宝鸡市', '首页', '', '违规插手工程,执纪审查', '2026-01-29 10:40:53.290604', '2026-01-29 10:40:53.290614', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (9, '中国民航大学飞行分校（飞行技术学院）招飞办公室主任崔雪超接受纪律审查', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1276/23027.htm', '清风网', '宝鸡市', '首页', '', '执纪审查', '2026-01-29 10:40:53.293837', '2026-01-29 10:40:53.293846', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (10, '陕西昌荣纺织有限责任公司原总会计师李光剑接受纪律审查和监察调查', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1276/23025.htm', '清风网', '宝鸡市', '首页', '', '执纪审查', '2026-01-29 10:40:53.296443', '2026-01-29 10:40:53.296451', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (11, '陕西昌荣纺织有限责任公司原副总经理杜剑峰接受纪律审查和监察调查', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1276/23026.htm', '清风网', '宝鸡市', '首页', '', '执纪审查', '2026-01-29 10:40:53.299910', '2026-01-29 10:40:53.299924', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (12, '宝鸡铁路技师学院原院长潘卫东严重违纪违法被开除党籍和公职', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1277/29484.htm', '清风网', '宝鸡市', '首页', '', '党纪处分', '2026-01-29 10:40:53.303757', '2026-01-29 10:40:53.303768', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (13, '法门文化景区管委会党工委原委员、管委会原副主任李丰安严重违纪违法被开', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1277/28528.htm', '清风网', '宝鸡市', '首页', '', '', '2026-01-29 10:40:53.307089', '2026-01-29 10:40:53.307100', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (14, '原宝鸡市计生局党组书记、局长王喆 严重违纪违法被开除党籍、取消退休待', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1277/28623.htm', '清风网', '宝鸡市', '首页', '', '党纪处分', '2026-01-29 10:40:53.309365', '2026-01-29 10:40:53.309375', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (15, '宝鸡市陇县中医医院原院长曹云超严重违纪违法被开除党籍和公职', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1277/26831.htm', '清风网', '宝鸡市', '首页', '', '教育医疗,党纪处分', '2026-01-29 10:40:53.312790', '2026-01-29 10:40:53.312800', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (16, '宝鸡市陈仓区粮油购销公司原法定代表人、总经理吴宝田、原会计董拉让严重', '', '', NULL, 'https://baoji.qinfeng.gov.cn/info/1277/23431.htm', '清风网', '宝鸡市', '首页', '', '', '2026-01-29 10:40:53.316220', '2026-01-29 10:40:53.316232', 'published', 0, 2, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (17, '吴堡县政府原副县长薛永升接受监察调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/77164.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.712452', '2026-01-29 10:40:53.712492', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (18, '中国中化西北橡胶塑料研究设计院有限公司原党委书记、总经理乐贵强…', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/77165.htm', '清风网', '咸阳市', '首页', '', '', '2026-01-29 10:40:53.727045', '2026-01-29 10:40:53.727080', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (19, '陕西中医药大学副校长缪峰接受纪律审查和监察调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/71960.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.737775', '2026-01-29 10:40:53.737816', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (20, '陕西农业发展集团有限公司原党委书记、董事长韩霁昌接受纪律审查和…', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/70744.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.757262', '2026-01-29 10:40:53.757332', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (21, '西安市生态环境局党委委员、西安市生态环境保护综合执法支队支队长…', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/70368.htm', '清风网', '咸阳市', '首页', '', '生态环保', '2026-01-29 10:40:53.778791', '2026-01-29 10:40:53.778845', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (22, '陕西省广播电视局原副局长刘生胜接受纪律审查和监察调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/70367.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.798748', '2026-01-29 10:40:53.798813', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (23, '西安市人大常委会原副主任康军接受纪律审查和监察调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/70083.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.817829', '2026-01-29 10:40:53.817883', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (24, '陕西省西安市人大常委会党组书记、主任韩松接受中央纪委国家监委纪…', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/69827.htm', '清风网', '咸阳市', '首页', '', '', '2026-01-29 10:40:53.828207', '2026-01-29 10:40:53.828221', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (25, '榆林市住房和城乡建设局原局长、二级巡视员雷亚成接受审查调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/69431.htm', '清风网', '咸阳市', '首页', '', '违规插手工程,执纪审查', '2026-01-29 10:40:53.831133', '2026-01-29 10:40:53.831145', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (26, '陕西省工业和信息化厅原副厅长蔡苏昌接受纪律审查和监察调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/69430.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.835932', '2026-01-29 10:40:53.835945', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (27, '榆林市人大常委会原党组成员、副主任王效力接受纪律审查和监察调查', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/66968.htm', '清风网', '咸阳市', '首页', '', '执纪审查', '2026-01-29 10:40:53.839650', '2026-01-29 10:40:53.839667', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (28, '青海省政协党组成员、副主席马丰胜接受中央纪委国家监委纪律审查和…', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/66215.htm', '清风网', '咸阳市', '首页', '', '', '2026-01-29 10:40:53.847072', '2026-01-29 10:40:53.847092', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (29, '中央宣传部原副部长张建春严重违纪违法被开除党籍和公职', '', '', NULL, 'https://xianyang.qinfeng.gov.cn/info/1055/66213.htm', '清风网', '咸阳市', '首页', '', '党纪处分', '2026-01-29 10:40:53.851782', '2026-01-29 10:40:53.851807', 'published', 0, 3, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (30, '合阳：组织纪检监察干部集...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/101595.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.647739', '2026-01-29 10:40:55.647751', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (31, '蒲城县纪委监委：全链条发...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/100334.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.650259', '2026-01-29 10:40:55.650270', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (32, '我市举办新提拔干部和年轻...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/99985.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.652984', '2026-01-29 10:40:55.652995', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (33, '临渭：开展新任纪检监察领...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/99796.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.656124', '2026-01-29 10:40:55.656137', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (34, '合阳：召开全县纪检监察系...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/98823.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.658796', '2026-01-29 10:40:55.658808', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (35, '【集中整治进行时】临渭：...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/97248.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.661066', '2026-01-29 10:40:55.661076', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (36, '蒲城：“五个一”上好新入...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/96708.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.663814', '2026-01-29 10:40:55.663826', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (37, '大荔县纪委监委召开2024年...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/96350.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.666171', '2026-01-29 10:40:55.666181', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (38, '富平：任前廉考为新任干部...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/96188.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.668772', '2026-01-29 10:40:55.668788', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (39, '华阴市岳庙街道：“五一”...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1025/95584.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.672020', '2026-01-29 10:40:55.672033', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (40, '强化对村巡察 促进解决基层...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/101585.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.674954', '2026-01-29 10:40:55.674968', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (41, '明纪释法丨严肃查处违规滥...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/101445.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.677691', '2026-01-29 10:40:55.677700', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (42, '中共中央印发《中国共产党...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/101254.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.680136', '2026-01-29 10:40:55.680147', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (43, '明纪释法丨准确认定处理侵...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/101079.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.683029', '2026-01-29 10:40:55.683052', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (44, '以案明纪释法|党员干部收受...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/100833.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.685954', '2026-01-29 10:40:55.685964', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (45, '三堂会审 | 收受管理和服务...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/100517.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.689215', '2026-01-29 10:40:55.689231', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (46, '理论视野丨以廉洁家风 涵养...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/87440.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.692026', '2026-01-29 10:40:55.692036', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (47, '渭南高新区：严守礼尚往来...', '', '', NULL, 'https://weinan.qinfeng.gov.cn/info/1105/76507.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.694430', '2026-01-29 10:40:55.694441', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (48, '渭南市住房和城乡建设局原党组书记、局长姬智武接受纪律...', '', '', '2023-03-21', 'https://weinan.qinfeng.gov.cn/info/1245/93986.htm', '清风网', '渭南市', '首页', '', '违规插手工程', '2026-01-29 10:40:55.696673', '2026-01-29 10:40:55.696681', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (49, '华阴市太华村华峰片区二组原组长杨新虎被移送检察机关审...', '', '', '2022-02-08', 'https://weinan.qinfeng.gov.cn/info/1245/88332.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.699924', '2026-01-29 10:40:55.699936', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (50, '中国通用技术集团下属中国轻工业品进出口集团有限公司原...', '', '', '2021-07-24', 'https://weinan.qinfeng.gov.cn/info/1245/81173.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.702518', '2026-01-29 10:40:55.702528', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (51, '渭南市临渭区人民法院审判委员会委员李亚红接受审查调查', '', '', '2021-04-28', 'https://weinan.qinfeng.gov.cn/info/1245/81174.htm', '清风网', '渭南市', '首页', '', '执纪审查', '2026-01-29 10:40:55.704765', '2026-01-29 10:40:55.704774', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (52, '韩城市人民法院审判监督庭原庭长贾克俭接受审查调查', '', '', '2021-04-27', 'https://weinan.qinfeng.gov.cn/info/1245/81175.htm', '清风网', '渭南市', '首页', '', '执纪审查', '2026-01-29 10:40:55.707711', '2026-01-29 10:40:55.707719', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (53, '渭南市纪委监委通报4起违反中央八项规定精神问题典型案例', '', '', '2023-12-28', 'https://weinan.qinfeng.gov.cn/info/1246/93987.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.710454', '2026-01-29 10:40:55.710462', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (54, '渭南市纪委监委通报10起酒驾醉驾典型案例', '', '', '2023-12-20', 'https://weinan.qinfeng.gov.cn/info/1246/93988.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.712769', '2026-01-29 10:40:55.712778', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (55, '渭南市纪委监委通报8起酒驾醉驾典型案例', '', '', '2023-12-18', 'https://weinan.qinfeng.gov.cn/info/1246/93989.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.716044', '2026-01-29 10:40:55.716058', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (56, '渭南市纪委监委通报3起群众身边腐败和作风问题典型案例', '', '', '2023-12-15', 'https://weinan.qinfeng.gov.cn/info/1246/93990.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.719240', '2026-01-29 10:40:55.719250', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (57, '渭南市纪委监委通报2起违规发展党员问题典型案例', '', '', '2023-12-13', 'https://weinan.qinfeng.gov.cn/info/1246/93991.htm', '清风网', '渭南市', '首页', '', '', '2026-01-29 10:40:55.722244', '2026-01-29 10:40:55.722253', 'published', 0, 5, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (58, '中国石油长庆油田公司技术检测中心原主任李国庆接受纪律审查和监察调查', '', '', '2025-12-05', 'https://yanan.qinfeng.gov.cn/info/1164/26753.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.402164', '2026-01-29 10:40:56.402181', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (59, '中国矿业大学（北京）原党委常委、副校长范中启接受审查调查', '', '', '2025-06-27', 'https://yanan.qinfeng.gov.cn/info/1164/26573.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.406125', '2026-01-29 10:40:56.406138', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (60, '延安市原土地统征管理办公室主任张剑君接受纪律审查和监察调查', '', '', '2025-04-10', 'https://yanan.qinfeng.gov.cn/info/1164/26483.htm', '清风网', '延安市', '首页', '', '违规插手工程,执纪审查', '2026-01-29 10:40:56.410719', '2026-01-29 10:40:56.410734', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (61, '延安市中级人民法院四级高级法官赵伟接受纪律审查和监察调查', '', '', '2024-09-24', 'https://yanan.qinfeng.gov.cn/info/1164/26191.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.418660', '2026-01-29 10:40:56.418684', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (62, '延安水务环保集团自来水有限公司原总经理李中华接受纪律审查和监察调查', '', '', '2024-07-26', 'https://yanan.qinfeng.gov.cn/info/1164/26426.htm', '清风网', '延安市', '首页', '', '执纪审查,生态环保', '2026-01-29 10:40:56.436040', '2026-01-29 10:40:56.436087', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (63, '延安市甘泉县人民法院原党组成员、执行局局长杨金成接受纪律审查和监察调查', '', '', '2024-06-25', 'https://yanan.qinfeng.gov.cn/info/1164/26085.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.458865', '2026-01-29 10:40:56.458928', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (64, '延安市甘泉县财政局原收费中心主任谢嘉平接受纪律审查和监察调查', '', '', '2024-01-19', 'https://yanan.qinfeng.gov.cn/info/1164/25871.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.483088', '2026-01-29 10:40:56.483139', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (65, '延安市黄陵中学原校长蔡永峰接受纪律审查和监察调查', '', '', '2024-01-05', 'https://yanan.qinfeng.gov.cn/info/1164/25843.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.495405', '2026-01-29 10:40:56.495447', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (66, '延安市人力资源和社会保障局原党组成员、副局长党鹏严重违纪违法被开除党籍', '', '', '2023-12-16', 'https://yanan.qinfeng.gov.cn/info/1164/25753.htm', '清风网', '延安市', '首页', '', '党纪处分', '2026-01-29 10:40:56.510053', '2026-01-29 10:40:56.510105', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (67, '延安市子长市粮油购销有限公司原经理李胜利接受纪律审查和监察调查', '', '', '2023-11-07', 'https://yanan.qinfeng.gov.cn/info/1164/25767.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.525983', '2026-01-29 10:40:56.526023', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (68, '延安市安塞区沿河湾镇财政所原所长张文伟接受纪律审查和监察调查', '', '', '2023-10-18', 'https://yanan.qinfeng.gov.cn/info/1164/25659.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.533743', '2026-01-29 10:40:56.533754', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (69, '延安市城市管理监督指挥中心原副主任杜月飞接受纪律审查和监察调查', '', '', '2023-10-08', 'https://yanan.qinfeng.gov.cn/info/1164/25654.htm', '清风网', '延安市', '首页', '', '执纪审查,市管干部', '2026-01-29 10:40:56.538074', '2026-01-29 10:40:56.538084', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (70, '延安市人力资源和社会保障局原党组成员、副局长党鹏接受纪律审查和监察调查', '', '', '2023-09-18', 'https://yanan.qinfeng.gov.cn/info/1164/25621.htm', '清风网', '延安市', '首页', '', '执纪审查', '2026-01-29 10:40:56.542353', '2026-01-29 10:40:56.542362', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (71, '甘泉县环境卫生和园林绿化管理站主任曹新接受纪律审查和监察调查', '', '', '2023-09-15', 'https://yanan.qinfeng.gov.cn/info/1164/25613.htm', '清风网', '延安市', '首页', '', '执纪审查,生态环保', '2026-01-29 10:40:56.546602', '2026-01-29 10:40:56.546612', 'published', 0, 6, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (72, '榆林市生态环境局子洲分局局长贺腾飞接受审查调查', '', '', '2025-12-15', 'https://yulin.qinfeng.gov.cn/info/1080/26457.htm', '清风网', '榆林市', '首页', '', '执纪审查,生态环保', '2026-01-29 10:40:56.923242', '2026-01-29 10:40:56.923254', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (73, '吴堡县政府原副县长薛永升接受监察调查', '', '', '2025-12-12', 'https://yulin.qinfeng.gov.cn/info/1080/26455.htm', '清风网', '榆林市', '首页', '', '执纪审查', '2026-01-29 10:40:56.928652', '2026-01-29 10:40:56.928665', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (74, '榆林市第一医院原院长冯丙东接受审查调查', '', '', '2025-09-08', 'https://yulin.qinfeng.gov.cn/info/1080/26278.htm', '清风网', '榆林市', '首页', '', '教育医疗,执纪审查', '2026-01-29 10:40:56.936562', '2026-01-29 10:40:56.936572', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (75, '定边县民政局原局长马保贵接受审查调查', '', '', '2025-07-07', 'https://yulin.qinfeng.gov.cn/info/1080/26127.htm', '清风网', '榆林市', '首页', '', '执纪审查', '2026-01-29 10:40:56.939615', '2026-01-29 10:40:56.939623', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (76, '神木市公安局尔林兔派出所所长杨金良接受审查调查', '', '', '2025-06-27', 'https://yulin.qinfeng.gov.cn/info/1080/26085.htm', '清风网', '榆林市', '首页', '', '执纪审查', '2026-01-29 10:40:56.943446', '2026-01-29 10:40:56.943458', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (77, '榆林市住房和城乡建设局原局长、二级巡视员雷亚成接受审查调查', '', '', '2025-06-20', 'https://yulin.qinfeng.gov.cn/info/1080/26064.htm', '清风网', '榆林市', '首页', '', '违规插手工程,执纪审查', '2026-01-29 10:40:56.947114', '2026-01-29 10:40:56.947125', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (78, '榆林市财政局党组成员、四级调研员张渝林接受审查调查', '', '', '2025-05-27', 'https://yulin.qinfeng.gov.cn/info/1080/26065.htm', '清风网', '榆林市', '首页', '', '执纪审查', '2026-01-29 10:40:56.950502', '2026-01-29 10:40:56.950512', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (79, '神木市档案局原局长闫晓庆接受审查调查', '', '', '2025-03-24', 'https://yulin.qinfeng.gov.cn/info/1080/25840.htm', '清风网', '榆林市', '首页', '', '执纪审查', '2026-01-29 10:40:56.953366', '2026-01-29 10:40:56.953375', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (80, '佳县人民医院原党支部书记、院长李红卫接受审查调查', '', '', '2025-03-20', 'https://yulin.qinfeng.gov.cn/info/1080/25817.htm', '清风网', '榆林市', '首页', '', '教育医疗,执纪审查', '2026-01-29 10:40:56.957191', '2026-01-29 10:40:56.957204', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (81, '绥德县四十里铺镇崔家圪崂村党支部书记、村委会主任郝建军接...', '', '', '2025-03-20', 'https://yulin.qinfeng.gov.cn/info/1080/25816.htm', '清风网', '榆林市', '首页', '', '', '2026-01-29 10:40:56.960603', '2026-01-29 10:40:56.960614', 'published', 0, 7, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (82, '中信银行呼和浩特分行原党委委员、行长助理王志忠接受审查调查', '', '', '2024-05-13', 'https://hanzhong.qinfeng.gov.cn/info/1007/29669.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.344980', '2026-01-29 10:40:57.344992', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (83, '略阳县卫健局原党组书记、局长、三级调研员胡荣昌接受纪律审查和监察调查', '', '', '2023-09-27', 'https://hanzhong.qinfeng.gov.cn/info/1007/29442.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.348905', '2026-01-29 10:40:57.348917', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (84, '汉中市南郑区政协党组原副书记、副主席、红庙镇党委原书记朱以荣被开除党籍和公职', '', '', '2021-08-16', 'https://hanzhong.qinfeng.gov.cn/info/1007/25999.htm', '清风网', '汉中市', '首页', '', '党纪处分', '2026-01-29 10:40:57.352652', '2026-01-29 10:40:57.352668', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (85, '陕西煤业化工集团有限责任公司原副总经理张丹力被开除党籍、取消退休待遇', '', '', '2021-08-13', 'https://hanzhong.qinfeng.gov.cn/info/1007/25987.htm', '清风网', '汉中市', '首页', '', '党纪处分', '2026-01-29 10:40:57.355754', '2026-01-29 10:40:57.355763', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (86, '汉中市公安局经济开发区分局党委委员、副局长白靖接受纪律审查和监察调查', '', '', '2021-06-16', 'https://hanzhong.qinfeng.gov.cn/info/1007/25692.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.359465', '2026-01-29 10:40:57.359475', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (87, '汉中市南郑区政协党组副书记、副主席、红庙镇党委书记朱以荣接受审查调查', '', '', '2021-03-26', 'https://hanzhong.qinfeng.gov.cn/info/1007/25389.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.363131', '2026-01-29 10:40:57.363139', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (88, '汉中市公安局原党委委员、副局长王雨团被开除党籍', '', '', '2020-12-30', 'https://hanzhong.qinfeng.gov.cn/info/1007/24924.htm', '清风网', '汉中市', '首页', '', '党纪处分', '2026-01-29 10:40:57.365932', '2026-01-29 10:40:57.365940', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (89, '西安市政公用建设投资集团有限公司原党委书记、董事长毛浓成接受审查调查', '', '', '2020-12-11', 'https://hanzhong.qinfeng.gov.cn/info/1007/24869.htm', '清风网', '汉中市', '首页', '', '违规插手工程,执纪审查', '2026-01-29 10:40:57.369497', '2026-01-29 10:40:57.369510', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (90, '汉中市宝汉高速公路项目协调办公室专职副主任韩文玉接受审查调查', '', '', '2020-11-16', 'https://hanzhong.qinfeng.gov.cn/info/1007/24703.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.373413', '2026-01-29 10:40:57.373423', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (91, '青海省副省长、海西蒙古族藏族自治州委书记、柴达木循环经济试验区党工委书记文国...', '', '', '2020-09-07', 'https://hanzhong.qinfeng.gov.cn/info/1007/24392.htm', '清风网', '汉中市', '首页', '', '', '2026-01-29 10:40:57.377198', '2026-01-29 10:40:57.377206', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (92, '咸阳市住房公积金管理中心党组书记、主任李晓强接受审查调查', '', '', '2020-06-29', 'https://hanzhong.qinfeng.gov.cn/info/1007/22764.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.379436', '2026-01-29 10:40:57.379444', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (93, '公安部党委委员、副部长孙力军接受中央纪委国家监委审查调查', '', '', '2020-04-20', 'https://hanzhong.qinfeng.gov.cn/info/1007/22763.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.382365', '2026-01-29 10:40:57.382373', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (94, '西乡县委副书记、县长李耕接受纪律审查和监察调查', '', '', '2019-11-25', 'https://hanzhong.qinfeng.gov.cn/info/1007/22765.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.386056', '2026-01-29 10:40:57.386068', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (95, '勉县县委常委、县政府副县长、党组副书记柳必成接受纪律审查和监察调查', '', '', '2019-11-25', 'https://hanzhong.qinfeng.gov.cn/info/1007/22762.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.389587', '2026-01-29 10:40:57.389601', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (96, '西乡县扶贫开发办公室主任全子强接受纪律审查和监察调查', '', '', '2019-07-04', 'https://hanzhong.qinfeng.gov.cn/info/1007/1007.htm', '清风网', '汉中市', '首页', '', '执纪审查,扶贫领域', '2026-01-29 10:40:57.393617', '2026-01-29 10:40:57.393627', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (97, '西乡县交通运输局局长张毅接受纪律审查和监察调查', '', '', '2019-07-04', 'https://hanzhong.qinfeng.gov.cn/info/1007/1006.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.396920', '2026-01-29 10:40:57.396930', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (98, '西乡县河道堤防管理站副站长余跃宏接受监察调查', '', '', '2019-07-04', 'https://hanzhong.qinfeng.gov.cn/info/1007/1005.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.399622', '2026-01-29 10:40:57.399630', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (99, '汉中市委常委秘书长统战部长牟晓非接受纪律审查和监察调查', '', '', '2019-07-03', 'https://hanzhong.qinfeng.gov.cn/info/1007/1004.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.402371', '2026-01-29 10:40:57.402379', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (100, '汉中市政协秘书长卢兴成等3名处级干部接受纪律审查和监察调查', '', '', '2019-07-03', 'https://hanzhong.qinfeng.gov.cn/info/1007/1003.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.407962', '2026-01-29 10:40:57.407972', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (101, '汉中市政协主席王隆庆接受纪律审查和监察调查', '', '', '2019-06-29', 'https://hanzhong.qinfeng.gov.cn/info/1007/1015.htm', '清风网', '汉中市', '首页', '', '执纪审查', '2026-01-29 10:40:57.410825', '2026-01-29 10:40:57.410832', 'published', 0, 8, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (102, '安康市恒口示范区生态环境局局长王敦贵接受审查调查', '', '', '2024-04-12', 'https://ankang.qinfeng.gov.cn/info/1117/30384.htm', '清风网', '安康市', '首页', '', '执纪审查,生态环保', '2026-01-29 10:40:57.808924', '2026-01-29 10:40:57.808946', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (103, '宁陕县人大常委会原副主任黄国庆接受审查调查', '', '', '2023-11-28', 'https://ankang.qinfeng.gov.cn/info/1117/29721.htm', '清风网', '安康市', '首页', '', '执纪审查', '2026-01-29 10:40:57.812909', '2026-01-29 10:40:57.812916', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (104, '旬阳市卫生健康局三级调研员李瑞清接受纪律审查和...', '', '', '2023-11-06', 'https://ankang.qinfeng.gov.cn/info/1117/29608.htm', '清风网', '安康市', '首页', '', '执纪审查', '2026-01-29 10:40:57.816822', '2026-01-29 10:40:57.816831', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (105, '紫阳县水利局原党委书记、局长曹仲之接受纪律审查...', '', '', '2023-09-28', 'https://ankang.qinfeng.gov.cn/info/1117/29484.htm', '清风网', '安康市', '首页', '', '执纪审查', '2026-01-29 10:40:57.819876', '2026-01-29 10:40:57.819885', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (106, '石泉县民政局党组书记、局长刘军接受纪律审查和监...', '', '', '2023-08-18', 'https://ankang.qinfeng.gov.cn/info/1117/29294.htm', '清风网', '安康市', '首页', '', '执纪审查', '2026-01-29 10:40:57.823527', '2026-01-29 10:40:57.823547', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (107, '白河县林业局原党委书记、局长阮家顺接受纪律审查...', '', '', '2023-08-03', 'https://ankang.qinfeng.gov.cn/info/1117/29224.htm', '清风网', '安康市', '首页', '', '执纪审查', '2026-01-29 10:40:57.827277', '2026-01-29 10:40:57.827286', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (108, '镇坪县工商业联合会主席张春平接受监察调查', '', '', '2023-06-05', 'https://ankang.qinfeng.gov.cn/info/1117/28965.htm', '清风网', '安康市', '首页', '', '执纪审查', '2026-01-29 10:40:57.829943', '2026-01-29 10:40:57.829950', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (109, '宁陕县教育体育和科技局原党委书记、局长   陈衍子...', '', '', '2023-07-10', 'https://ankang.qinfeng.gov.cn/info/1297/29806.htm', '清风网', '安康市', '首页', '', '教育医疗', '2026-01-29 10:40:57.833794', '2026-01-29 10:40:57.833804', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (110, '安康市文化和旅游广电局原党组书记、局长杨海波受...', '', '', '2022-06-01', 'https://ankang.qinfeng.gov.cn/info/1297/26611.htm', '清风网', '安康市', '首页', '', '', '2026-01-29 10:40:57.836707', '2026-01-29 10:40:57.836714', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (111, '原安康市文化产业发展中心副主任、市演艺影视公司...', '', '', '2021-10-22', 'https://ankang.qinfeng.gov.cn/info/1297/24916.htm', '清风网', '安康市', '首页', '', '', '2026-01-29 10:40:57.840202', '2026-01-29 10:40:57.840215', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (112, '安康市公安局汉滨分局交通管理大队江北交警中队原...', '', '', '2021-08-13', 'https://ankang.qinfeng.gov.cn/info/1297/24167.htm', '清风网', '安康市', '首页', '', '', '2026-01-29 10:40:57.843038', '2026-01-29 10:40:57.843048', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (113, '镇坪县人大常委会党组成员、副主任韦树辉严重违纪...', '', '', '2018-08-17', 'https://ankang.qinfeng.gov.cn/info/1297/23794.htm', '清风网', '安康市', '首页', '', '', '2026-01-29 10:40:57.846186', '2026-01-29 10:40:57.846195', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (114, '镇坪县财政局政府采购管理股股长程斌严重违纪违法...', '', '', '2018-08-17', 'https://ankang.qinfeng.gov.cn/info/1297/23795.htm', '清风网', '安康市', '首页', '', '违规插手工程', '2026-01-29 10:40:57.848400', '2026-01-29 10:40:57.848409', 'published', 0, 9, NULL, NULL, '', 0, '');
INSERT INTO `news` VALUES (115, '市中心医院原院长、党委副书记王永堂因违纪受到党...', '', '', '2017-07-18', 'https://ankang.qinfeng.gov.cn/info/1297/23796.htm', '清风网', '安康市', '首页', '', '教育医疗', '2026-01-29 10:40:57.851286', '2026-01-29 10:40:57.851297', 'published', 0, 9, NULL, NULL, '', 0, '');

-- ----------------------------
-- Table structure for news_manual_tags
-- ----------------------------
DROP TABLE IF EXISTS `news_manual_tags`;
CREATE TABLE `news_manual_tags`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `news_id` bigint NOT NULL,
  `tag_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `news_manual_tags_news_id_tag_id_27bae3ae_uniq`(`news_id` ASC, `tag_id` ASC) USING BTREE,
  INDEX `news_manual_tags_tag_id_9c5f5a1f_fk_tag_id`(`tag_id` ASC) USING BTREE,
  CONSTRAINT `news_manual_tags_news_id_8345b2a8_fk_news_id` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `news_manual_tags_tag_id_9c5f5a1f_fk_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of news_manual_tags
-- ----------------------------

-- ----------------------------
-- Table structure for news_tags
-- ----------------------------
DROP TABLE IF EXISTS `news_tags`;
CREATE TABLE `news_tags`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `news_id` bigint NOT NULL,
  `tag_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `news_tags_news_id_tag_id_7fb1b7fb_uniq`(`news_id` ASC, `tag_id` ASC) USING BTREE,
  INDEX `news_tags_tag_id_b25e7549_fk_tag_id`(`tag_id` ASC) USING BTREE,
  CONSTRAINT `news_tags_news_id_06acc240_fk_news_id` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `news_tags_tag_id_b25e7549_fk_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 95 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of news_tags
-- ----------------------------
INSERT INTO `news_tags` VALUES (1, 1, 14);
INSERT INTO `news_tags` VALUES (2, 2, 14);
INSERT INTO `news_tags` VALUES (3, 3, 8);
INSERT INTO `news_tags` VALUES (4, 3, 14);
INSERT INTO `news_tags` VALUES (5, 4, 16);
INSERT INTO `news_tags` VALUES (6, 5, 15);
INSERT INTO `news_tags` VALUES (7, 6, 15);
INSERT INTO `news_tags` VALUES (8, 7, 14);
INSERT INTO `news_tags` VALUES (9, 8, 6);
INSERT INTO `news_tags` VALUES (10, 8, 14);
INSERT INTO `news_tags` VALUES (11, 9, 14);
INSERT INTO `news_tags` VALUES (12, 10, 14);
INSERT INTO `news_tags` VALUES (13, 11, 14);
INSERT INTO `news_tags` VALUES (14, 12, 15);
INSERT INTO `news_tags` VALUES (15, 14, 15);
INSERT INTO `news_tags` VALUES (16, 15, 8);
INSERT INTO `news_tags` VALUES (17, 15, 15);
INSERT INTO `news_tags` VALUES (18, 17, 14);
INSERT INTO `news_tags` VALUES (19, 19, 14);
INSERT INTO `news_tags` VALUES (20, 20, 14);
INSERT INTO `news_tags` VALUES (21, 21, 9);
INSERT INTO `news_tags` VALUES (22, 22, 14);
INSERT INTO `news_tags` VALUES (23, 23, 14);
INSERT INTO `news_tags` VALUES (24, 25, 6);
INSERT INTO `news_tags` VALUES (25, 25, 14);
INSERT INTO `news_tags` VALUES (26, 26, 14);
INSERT INTO `news_tags` VALUES (27, 27, 14);
INSERT INTO `news_tags` VALUES (28, 29, 15);
INSERT INTO `news_tags` VALUES (29, 48, 6);
INSERT INTO `news_tags` VALUES (30, 51, 14);
INSERT INTO `news_tags` VALUES (31, 52, 14);
INSERT INTO `news_tags` VALUES (32, 58, 14);
INSERT INTO `news_tags` VALUES (33, 59, 14);
INSERT INTO `news_tags` VALUES (34, 60, 6);
INSERT INTO `news_tags` VALUES (35, 60, 14);
INSERT INTO `news_tags` VALUES (36, 61, 14);
INSERT INTO `news_tags` VALUES (37, 62, 9);
INSERT INTO `news_tags` VALUES (38, 62, 14);
INSERT INTO `news_tags` VALUES (39, 63, 14);
INSERT INTO `news_tags` VALUES (40, 64, 14);
INSERT INTO `news_tags` VALUES (41, 65, 14);
INSERT INTO `news_tags` VALUES (42, 66, 15);
INSERT INTO `news_tags` VALUES (43, 67, 14);
INSERT INTO `news_tags` VALUES (44, 68, 14);
INSERT INTO `news_tags` VALUES (45, 69, 11);
INSERT INTO `news_tags` VALUES (46, 69, 14);
INSERT INTO `news_tags` VALUES (47, 70, 14);
INSERT INTO `news_tags` VALUES (48, 71, 9);
INSERT INTO `news_tags` VALUES (49, 71, 14);
INSERT INTO `news_tags` VALUES (50, 72, 9);
INSERT INTO `news_tags` VALUES (51, 72, 14);
INSERT INTO `news_tags` VALUES (52, 73, 14);
INSERT INTO `news_tags` VALUES (53, 74, 8);
INSERT INTO `news_tags` VALUES (54, 74, 14);
INSERT INTO `news_tags` VALUES (55, 75, 14);
INSERT INTO `news_tags` VALUES (56, 76, 14);
INSERT INTO `news_tags` VALUES (57, 77, 6);
INSERT INTO `news_tags` VALUES (58, 77, 14);
INSERT INTO `news_tags` VALUES (59, 78, 14);
INSERT INTO `news_tags` VALUES (60, 79, 14);
INSERT INTO `news_tags` VALUES (61, 80, 8);
INSERT INTO `news_tags` VALUES (62, 80, 14);
INSERT INTO `news_tags` VALUES (63, 82, 14);
INSERT INTO `news_tags` VALUES (64, 83, 14);
INSERT INTO `news_tags` VALUES (65, 84, 15);
INSERT INTO `news_tags` VALUES (66, 85, 15);
INSERT INTO `news_tags` VALUES (67, 86, 14);
INSERT INTO `news_tags` VALUES (68, 87, 14);
INSERT INTO `news_tags` VALUES (69, 88, 15);
INSERT INTO `news_tags` VALUES (70, 89, 6);
INSERT INTO `news_tags` VALUES (71, 89, 14);
INSERT INTO `news_tags` VALUES (72, 90, 14);
INSERT INTO `news_tags` VALUES (73, 92, 14);
INSERT INTO `news_tags` VALUES (74, 93, 14);
INSERT INTO `news_tags` VALUES (75, 94, 14);
INSERT INTO `news_tags` VALUES (76, 95, 14);
INSERT INTO `news_tags` VALUES (78, 96, 7);
INSERT INTO `news_tags` VALUES (77, 96, 14);
INSERT INTO `news_tags` VALUES (79, 97, 14);
INSERT INTO `news_tags` VALUES (80, 98, 14);
INSERT INTO `news_tags` VALUES (81, 99, 14);
INSERT INTO `news_tags` VALUES (82, 100, 14);
INSERT INTO `news_tags` VALUES (83, 101, 14);
INSERT INTO `news_tags` VALUES (84, 102, 9);
INSERT INTO `news_tags` VALUES (85, 102, 14);
INSERT INTO `news_tags` VALUES (86, 103, 14);
INSERT INTO `news_tags` VALUES (87, 104, 14);
INSERT INTO `news_tags` VALUES (88, 105, 14);
INSERT INTO `news_tags` VALUES (89, 106, 14);
INSERT INTO `news_tags` VALUES (90, 107, 14);
INSERT INTO `news_tags` VALUES (91, 108, 14);
INSERT INTO `news_tags` VALUES (92, 109, 8);
INSERT INTO `news_tags` VALUES (93, 114, 6);
INSERT INTO `news_tags` VALUES (94, 115, 8);

-- ----------------------------
-- Table structure for region
-- ----------------------------
DROP TABLE IF EXISTS `region`;
CREATE TABLE `region`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `domain` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `code`(`code` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of region
-- ----------------------------
INSERT INTO `region` VALUES (1, 'xian', '西安市', 'xian.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (2, 'baoji', '宝鸡市', 'baoji.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (3, 'xianyang', '咸阳市', 'xianyang.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (4, 'tongchuan', '铜川市', 'tongchuan.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (5, 'weinan', '渭南市', 'weinan.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (6, 'yanan', '延安市', 'yanan.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (7, 'yulin', '榆林市', 'yulin.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (8, 'hanzhong', '汉中市', 'hanzhong.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (9, 'ankang', '安康市', 'ankang.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (10, 'shangluo', '商洛市', 'shangluo.qinfeng.gov.cn', 'scdc.htm', 1, 0);
INSERT INTO `region` VALUES (11, 'yangling', '杨凌示范区', 'yangling.qinfeng.gov.cn', 'scdc.htm', 1, 0);

-- ----------------------------
-- Table structure for supervision_item
-- ----------------------------
DROP TABLE IF EXISTS `supervision_item`;
CREATE TABLE `supervision_item`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `year` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `month` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `core_keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `synonyms` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `context_words` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `standard` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sort` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `created_by_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `supervision_item_name_year_month_ac772111_uniq`(`name` ASC, `year` ASC, `month` ASC) USING BTREE,
  INDEX `supervision_item_category_id_6d54e8bf_fk_tag_category_id`(`category_id` ASC) USING BTREE,
  INDEX `supervision_item_created_by_id_d8436c8a_fk_auth_user_id`(`created_by_id` ASC) USING BTREE,
  CONSTRAINT `supervision_item_category_id_6d54e8bf_fk_tag_category_id` FOREIGN KEY (`category_id`) REFERENCES `tag_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `supervision_item_created_by_id_d8436c8a_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of supervision_item
-- ----------------------------

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `keywords` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_auto` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sort` int NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tag_category_id_702f51c7_fk_tag_category_id`(`category_id` ASC) USING BTREE,
  CONSTRAINT `tag_category_id_702f51c7_fk_tag_category_id` FOREIGN KEY (`category_id`) REFERENCES `tag_category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (1, '违反八项规定', '公款吃喝,礼品礼金,违规发放,公车私用,公款旅游', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (2, '形式主义官僚主义', '形式主义,官僚主义,不作为,慢作为,乱作为,推诿扯皮', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (3, '贪污受贿', '贪污,受贿,挪用公款,侵占挪用', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (4, '滥用职权', '滥用职权,玩忽职守,徇私枉法', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (5, '失职渎职', '失职,渎职,监管不力,履职不力', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (6, '违规插手工程', '工程,招标,采购,土地,建设', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (7, '扶贫领域', '扶贫,脱贫,惠农,低保,困难群众', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (8, '教育医疗', '教育,学校,医疗,医保,医院,招生', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (9, '生态环保', '生态,环保,污染,环境,督察', '', '#00D2FF', 1, 1, 0, 1);
INSERT INTO `tag` VALUES (10, '省管干部', '省管,副省级,正厅级,副厅级', '', '#00D2FF', 1, 1, 0, 2);
INSERT INTO `tag` VALUES (11, '市管干部', '市管,正处级,副处级', '', '#00D2FF', 1, 1, 0, 2);
INSERT INTO `tag` VALUES (12, '县管干部', '县管,正科级,副科级', '', '#00D2FF', 1, 1, 0, 2);
INSERT INTO `tag` VALUES (13, '基层干部', '科员,办事员,村干部,社区干部', '', '#00D2FF', 1, 1, 0, 2);
INSERT INTO `tag` VALUES (14, '执纪审查', '接受纪律审查,接受监察调查,审查调查', '', '#00D2FF', 1, 1, 0, 3);
INSERT INTO `tag` VALUES (15, '党纪处分', '开除党籍,严重警告,警告,留党察看', '', '#00D2FF', 1, 1, 0, 3);
INSERT INTO `tag` VALUES (16, '政务处分', '开除公职,政务撤职,政务降级,政务警告', '', '#00D2FF', 1, 1, 0, 3);
INSERT INTO `tag` VALUES (17, '双开', '开除党籍开除公职,双开', '', '#00D2FF', 1, 1, 0, 3);

-- ----------------------------
-- Table structure for tag_category
-- ----------------------------
DROP TABLE IF EXISTS `tag_category`;
CREATE TABLE `tag_category`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `sort` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag_category
-- ----------------------------
INSERT INTO `tag_category` VALUES (1, '违规类型', '', '#FF6B9D', 0);
INSERT INTO `tag_category` VALUES (2, '干部级别', '', '#00D2FF', 0);
INSERT INTO `tag_category` VALUES (3, '案件状态', '', '#9933FF', 0);

SET FOREIGN_KEY_CHECKS = 1;
