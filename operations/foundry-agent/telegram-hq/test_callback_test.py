import unittest
from callback_test import check_callback, process

P = {"test_id":"abcdef0123456789","chat_id":"123", "message_id":77}

def event(uid, data="test_yes:abcdef0123456789", chat_id=123, msg=77):
    return {"update_id":uid,"callback_query":{
        "id":f"cb-{uid}", "data":data,
        "message":{"message_id":msg,"chat":{"id":chat_id}}}}

class CallbackTests(unittest.TestCase):
    def test_exact_binding(self):
        self.assertEqual(check_callback(event(1)["callback_query"],P),"APPROVE_TEST")
        self.assertEqual(check_callback(event(2,"test_no:abcdef0123456789")["callback_query"],P),"REJECT_TEST")
    def test_wrong_chat_rejected(self):
        self.assertIsNone(check_callback(event(1,chat_id=124)["callback_query"],P))
    def test_wrong_message_rejected(self):
        self.assertIsNone(check_callback(event(1,msg=78)["callback_query"],P))
    def test_wrong_nonce_rejected(self):
        self.assertIsNone(check_callback(event(1,data="test_yes:wrong")["callback_query"],P))
    def test_once_only(self):
        calls=[]
        answer=lambda *args:calls.append(args)
        result=process([event(4),event(5)],P,{"offset":0,"decision":None},answer)
        self.assertEqual(result,{"offset":6,"decision":"APPROVE_TEST"})
        self.assertEqual(len(calls),2)
        self.assertEqual(process([event(4)],P,result,answer),result)
    def test_reject_is_not_approval(self):
        result=process([event(1,"test_no:abcdef0123456789")],P,{"offset":0,"decision":None},lambda *args:None)
        self.assertEqual(result["decision"],"REJECT_TEST")
    def test_no_ack_no_commit(self):
        with self.assertRaises(RuntimeError):
            process([event(1)],P,{"offset":0,"decision":None},lambda *args:(_ for _ in ()).throw(RuntimeError()))
    def test_ignores_unrelated(self):
        result=process([event(8,data="other")],P,{"offset":0,"decision":None},lambda *args:None)
        self.assertIsNone(result["decision"])
        self.assertEqual(result["offset"],9)

if __name__=="__main__":
    unittest.main()
