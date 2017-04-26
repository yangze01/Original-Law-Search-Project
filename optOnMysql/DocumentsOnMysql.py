#coding=utf-8
import pymysql
from optOnMysql import *
from DocumentUnit import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DocumentsOnMysql(object):
    def __init__(self):
        self.opt_OnMySql = OptOnMysql()

    def findById(self,id):
        cur = self.opt_OnMySql.exeQuery("select * from document where _id = '%d'" %id)
        it = cur.fetchone()
        # print(it)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")#
        if it == None:
            # print("there is nothing found")
            return 0
        else:
            # print(it[5])
            print('\n       '.join(it[5].split('|')))
            return 1

    def getById(self, id):
        cur = self.opt_OnMySql.exeQuery("select * from document where _id = '%d'" % id)
        it = cur.fetchone()
        # print(it)
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")#
        if it == None:
            # print("there is nothing found")
            return None
        else:
            # print(it[5])
            # print('\n       '.join(it[5].split('|')))
            return it

    def findbycriminal(self, crim):
        '''
        :param crim: 罪名
        :return: criminal cursor of data
        '''
        cur = self.opt_OnMySql.exeQuery("select * from document where criminal = '%s'" %crim)
        it = cur.fetchall()
        if it == None:
            print("No data for %s" %crim)
        else:
            print("return data")
            return it







    def findall(self):
        cur = self.opt_OnMySql.exeQuery("select * from document")
        it = cur.fetchall()
        if it == None:
            print("this is now data")
            return it
        else:
            print("fetch all data")
            return it

    def insertOneDocuments(self,document_unit):
        '''
            description:
                 insert one document into mysql
            input:
                document_unit:
                    dict of document to be inserted
            output:
                num of insert document
        '''
        # self.old_document = self.findById(document_unit['_id'])
        # if self.old_document:
        #
        #     print("document exists")
        #     return 1
        # else:
        #     # print("++++++++~~~~~~~~=================----------------")
        sta = 0
        try:
            sql = "insert into document (title, court, url, content, criminal, date) values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".\
                format(document_unit["title"], document_unit["court"], document_unit["url"], document_unit["content"].encode('utf8'), document_unit["criminal"], document_unit["date"])
            sta = self.opt_OnMySql.exeUpdate(sql)
            # print(sql)
            # if sta == 1:
            # print("insert success!")
        except:
                print("insert failed!")
                print("the content length is :"+ str(len(document_unit["content"])))
                for i,k in document_unit.items():
                    print(str(i) + " : " + str(k))
                    print(len(k))
                    # print(k)
        # sta = self.opt_OnMySql.exeUpdate("insert into test (id,title) values(%d"%(int(document_unit["id"]))+",'"+document_unit["title"]+"')")
        return sta

    def deleteById(self,id):
        sta = self.opt_OnMySql.exeDeleteById("delete from document where id='%d'"%id)
        return sta

    def deleteByIds(self,ids):
        sta = 0
        for eachID in ids:
            sta += self.deleteById(eachID)
        return sta

    def connClose(self):
        self.opt_OnMySql.connClose()

if __name__ == "__main__":
    # print(1)
    document_unit = dict()
    # document_unit["_id"] = 2
    document_unit["title"] = "叶某交通肇事罪二审刑事裁定书"
    document_unit["court"] = "安徽省合肥市中级人民法院"
    document_unit["date"] = "2015-06-05"
    document_unit["url"] = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=eff7f53c-b647-11e3-84e9-5cf3fc0c2c18"
    # print(len(document_unit["url"]))
    document_unit["content"] = "安徽省合肥市中级人民法院|刑 事 裁 定 书|（2015）合刑终字第00256号|原公诉机关合肥市瑶海区人民检察院。|上诉人（原审被告人）叶某，无业。因涉嫌犯交通肇事罪于2014年12月9日被合肥市公安局取保候审，2015年3月27日被合肥市瑶海区人民法院取保候审，同年4月10日被合肥市瑶海区人民法院决定逮捕，同日由合肥市公安局执行逮捕。现羁押于合肥市第一看守所。|合肥市瑶海区人民法院审理合肥市瑶海区人民检察院指控原审被告人叶某犯交通肇事罪一案，于2015年4月13日作出（2015）瑶刑初字第00293号刑事判决。原审被告人叶某不服，提出上诉。本院依法组成合议庭，经阅卷、讯问上诉人，认为本案事实清楚，决定不开庭审理。本案现已审理终结。|原判认定：2014年11月13日2时50分许，被告人叶某醉酒后驾驶赣E×××××号宝马轿车，沿合肥市北一环路由西向东行驶至瑶海区站西路桥下穿桥附近时，因操作不当，赣E×××××号轿车碰撞到道路中间隔离护栏，导致方向失控后又碰撞到道路南侧的防护墙，造成被告人叶某及车辆乘坐人徐某、潘某受伤及车辆受损、隔离栏损坏。被害人徐某（女，1992年2月15日出生）经医院抢救无效于2014年12月3日死亡。经公安机关认定，被告人叶某承担此次事故的全部责任。|另查明，事故发生后，合肥市公安局交通警察支队瑶海大队民警接到附近群众电话报警后赶至案发现场，被告人叶某及被害人徐某已被120救护车送往医院救治，公安民警对现场勘查完毕后，遂赶至合肥市第二人民医院对被告人叶某抽血待检，后将其带至公安机关接受调查。经检测，被告人叶某血液中乙醇含量为118mg／100ml，属醉酒驾驶。经安徽同德司法鉴定所鉴定，被害人徐某系道路交通事故致特重度颅脑损伤继发多器官功能衰竭死亡。案发后，被告人叶某与被害人徐某的亲属达成赔偿协议，除已支付的医疗费外，由被告人叶某另外一次性赔偿给被害人徐某亲属各项经济损失共计人民币42万元（已即时付清），被害人徐某的亲属对被告人叶某表示谅解，建议司法机关对其免予刑事处罚。|原判认定上述事实的证据有：被告人叶某的供述、证人刘某、潘某、李某的证言、辨认笔录、现场勘验检查笔录、现场图及照片、道路交通事故认定书、尸体检验报告、人体乙醇含量检验报告书、涉案车辆交通事故技术鉴定意见书、死亡医学证明书、医院门诊病历、视听资料、机动车驾驶证及行驶证查询记录、情况说明、归案经过、户籍证明、协议书、谅解书、银行汇款单据等。|原判认为：被告人叶某违反交通运输管理法规，醉酒后驾驶机动车辆在道路上行驶，且操作不当，以致发生交通事故，造成一人死亡的严重后果，并负事故的全部责任，其行为已构成交通肇事罪。被告人叶某归案后如实供述自己的罪行，庭审中自愿认罪，可从轻处罚。被告人叶某案发后积极赔偿被害人徐某亲属的经济损失，并取得被害人亲属的谅解，可酌情从轻处罚。但被告人叶某醉酒后驾驶机动车发生交通事故，又可酌情从重处罚。依照《中华人民共和国刑法》第一百三十三条、第六十七条第三款、第六十一条规定，判决：被告人叶某犯交通肇事罪，判处有期徒刑十个月。|原审被告人叶某的上诉请求和理由为：一审量刑过重。|经审理查明：原判认定上诉人叶某犯交通肇事罪的事实，已被一审判决列举的证据证实，所列证据经一审当庭举证、质证，合法有效。本院审理中，上诉人叶某未提出新的证据，本院对一审判决认定的事实及相关证据予以确认。|关于上诉人叶某认为一审量刑过重的上诉理由，经查，一审在对上诉人叶某量刑时已考虑其如实供述、自愿认罪、取得被害人亲属谅解等情节，综合量刑对其从轻处罚，判决并无不当，上诉人叶某的上诉理由不能成立，本院不予支持。|本院认为：上诉人叶某违反交通运输管理法规，醉酒后驾驶机动车辆在道路上行驶，操作不当发生交通事故，造成一人死亡，负事故的全部责任，其行为已构成交通肇事罪，依法应予惩处。上诉人叶某醉酒后驾驶机动车发生交通事故，负事故的全部责任，可酌情从重处罚。上诉人叶某归案后如实供述自己的罪行，自愿认罪，可从轻处罚。上诉人叶某案发后积极赔偿被害人亲属的经济损失，并取得被害人亲属的谅解，可酌情从轻处罚。原判认定上诉人叶某犯交通肇事罪的事实清楚，证据确实充分，适用法律正确，量刑适当。审判程序合法。依照《中华人民共和国刑事诉讼法》第二百二十五条第一款第（一）项之规定，裁定如下：|驳回上诉，维持原判。|本裁定为终审裁定。|审　判　长　　张　恒|审　判　员　　陆文波|代理审判员　　董雪美|二〇一五年六月五日|书　记　员　　黄圣全|附：相关法律条文|《中华人民共和国刑事诉讼法》第二百二十五条第一款第（一）项原判决认定事实和适用法律正确、量刑适当的，应当裁定驳回上诉或者抗诉，维持原判。"
    document_unit["criminal"] = "交通肇事罪"

    # print(document_unit)
    opt = DocumentsOnMysql()

    opt.insertOneDocuments(document_unit)
    # it = opt.findbycriminal(u"抢劫罪")
    # print(len(it))

    # for i in it[0:5]:
    #     print('\n'.join(i[5].split('|')))
        # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    opt.connClose()
    # it = opt.findall()
    # print(len(it[0]))
    # opt.findById(2005)
