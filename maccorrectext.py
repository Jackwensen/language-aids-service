from pycorrector.macbert.macbert_corrector import MacBertCorrector

corrector = MacBertCorrector("shibing624/macbert4csc-base-chinese").macbert_correct

def in_door(input):
    # 输入
    originalText = input
    # 纠正文本输出
    suggestion = corrector(originalText)[0]
    print(suggestion)
    return suggestion