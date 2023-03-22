from scraper import update_articles, update_tweets, prev_articles_list, prev_tweets_list

__all__ = ['update_articles', 'update_tweets', 'prev_articles_list', 'prev_tweets_list']

#all 이라는 변수는 해당 모듈에서 import될 수 있는 함수들의 이름을
# 리스트로 지정하는 것입니다. 즉, 이 리스트에 포함되지 않은
# 함수는 다른 파일에서 import될 수 없습니다. 이 변수는 코드의
# 가독성을 높이고, 모듈 사용자에게 제공되는 함수들의 명확한 목록을
# 제공하는 데 도움이 됩니다.

'''
def function_one():
    print("This is function one.")

def function_two():
    print("This is function two.")

def function_three():
    print("This is function three.")

__all__ = ['function_one', 'function_two']

다른 파일에서 example_module 모듈을 사용할 때, 
function_one과 function_two만 import하고 싶다면:

from example_module import function_one, function_two

# 이제 function_one과 function_two만 사용 가능합니다.

만약 function_three를 import하려고 시도하면,
다음과 같은 에러가 발생할 것입니다:

NameError: name 'function_three' is not defined

'''

'''
네, __all__ 리스트를 정의하지 않아도 모듈의 함수와 변수들은 import가 가능합니다.

그러나, __all__ 리스트를 명시적으로 정의하면, 해당 모듈을 import하는 다른 코드에서 
사용 가능한 함수와 변수들의 리스트를 제공하게 됩니다. 이렇게 함으로써, 모듈을 사용하는 
다른 코드에서 잘못된 이름으로 함수나 변수를 사용하는 경우를 방지할 수 있습니다.

또한, from module import * 형태로 모듈을 import하는 경우, __all__ 리스트에 명시된 
함수와 변수만 import됩니다. 이는 모듈의 namespace를 깨끗하게 유지하고, 
코드의 가독성을 높이는 데에 도움을 줍니다.
'''