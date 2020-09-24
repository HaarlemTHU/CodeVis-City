# antlr4入门

ANTLR4 是一个非常厉害的程序/库，可以用来生成 Lexer 和 Parser，而且生成的接口非常易用。昨天匆匆把 [The Definitive ANTLR 4 Reference](https://pragprog.com/book/tpantlr2/the-definitive-antlr-4-reference) 扫了一遍，现在把一些常用的东西记下来。

#### 安装

```
$ cd /usr/local/lib
$ curl -O http://www.antlr.org/download/antlr-4.5-complete.jar

$ vim ~/.zshrc # or vim ~/.bashrc
export CLASSPATH=".:/usr/local/lib/antlr-4.5-complete.jar:$CLASSPATH"
alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.5-complete.jar:$CLASSPATH" org.antlr.v4.Tool'
alias grun='java org.antlr.v4.runtime.misc.TestRig'
$ . ~/.zshrc # or restart the terminal
```

#### 语法

最重要的一点是，官方已经提供了非常多的常用的语言的语法文件了，拿来看看可以学到很多，甚至可以删删改改直接拿来用： <https://github.com/antlr/grammars-v4>

- `grammar` 名称和文件名要一致
- Parser 规则（即 non-terminal）以小写字母开始
- Lexer 规则（即 terminal）以大写字母开始
- 所有的 Lexer 规则无论写在哪里都会被重排到 Parser 规则之后
- 所有规则中若有冲突，先出现的规则优先匹配
- 用 `'string'` 单引号引出字符串
- `|` 用于分隔两个产生式，`(a|b)` 括号用于指定子产生式，`?+*`用法同正则表达式
- 在产生式后面 `# label` 可以给某条产生式命名，在生成的代码中即可根据标签分辨不同产生式
- 不需要指定开始符号
- 规则以分号终结
- `/* block comment */` 以及 `// line comment`
- 默认的左结合，可以用 `<assoc=right>` 指定右结合
- 可以处理直接的左递归，不能处理间接的左递归
- 如果用 `MUL: '*';` 指定了某个字符串的名字，在程序里面就能用这个名字了
- 用 `fragment` 可以给 Lexer 规则中的公共部分命名

例子：

```
stmt:   expr NEWLINE                    # printExpr
    |   ID '=' expr NEWLINE             # assign
    |   NEWLINE                         # blank
    ;

expr:   <assoc=right> expr op='^' expr  # pow
    |   expr op=('*'|'/') expr          # mulDiv
    |   expr op=('+'|'-') expr          # addSub
    |   INT                             # int
    |   ID                              # id
    |   '(' expr ')'                    # parens

MUL : '*';
DIV : '/';
ADD : '+';
SUB : '-';
ID  : Letter LetterOrDigit*
fragment Letter: [a-zA-Z_]
fragment Digit: [0-9]
fragment LetterOrDigit: Letter | Digit
NEWLINE: '\r'? '\n'
WS  : [ \t]+ -> skip
```

Reference:

- Chapter 4     
  - 1 Matching an Arithmetic Expression Language
  - 2 Building a Calculator Using a Visitor
- Chapter 5     
  - 4 Dealing with Precedence, Left Recursion, and Associativity
  - 5 Recognizing Common Lexical Structures

#### 常见 Lexer 规则

```
//------ Puncuation
call : ID '(' exprList ')' ;
// or define token labels
call : ID LP exprList RP ;
LP   : '(';
RP   : ')';

//------ Keywords
returnStmt : 'return' expr ';' ;

//------ Identifiers
ID : ID_LETTER (ID_LETTER | DIGIT)* ;
fragment ID_LETTER : 'a'..'z' | 'A'..'Z' | '_' ;
fragment DIGIT : '0'..'9';

//------ Numbers
INT   : DIGIT+ ;
FLOAT : DIGIT+ '.' DIGIT*
      | '.' DIGIT+
      ;

//------ Strings
STRING : '"' (ESC | .)*? '"' ;
fragment ESC : '\\' [btnr"\\] ;  // \b, \t, \n, ...

//------ Comments
LINE_COMMENT  : '//' .*? '\n' -> skip;
BLOCK_COMMENT : '/*' .*? '*/' -> skip;

//------ Whitespace
WS : [ \t\n\r]+ -> skip
```

Reference:

- Chapter 5     
  - 5 Recognizing Common Lexical Structures

#### 整合到自己的程序中

ANTLR 4 提供了 Visitor 和 Listener 两种模式，通过这两种模式可以很轻松地把 Parser 的结果做各种处理。ANTLR 4 默认会生成 Listener 模式，如果不需要要加上 `-no-listener`，如果要生成 Visitor 模式要加上 `-visitor`。

```
$ antlr4 -visitor Calc.g4
$ ls
Calc.g4               CalcBaseVisitor.java  CalcListener.java
Calc.tokens           CalcLexer.java        CalcParser.java
CalcBaseListener.java CalcLexer.tokens      CalcVisitor.java
```

运行 ANTLR 4 会生成以下文件：

- `<Grammar>Lexer.java`: Lexer
- `<Grammar>Parser.java`: Parser
- `<Grammar>Listener.java`: Listener 接口
- `<Grammar>BaseListener.java`: Listener 默认实现
- `<Grammar>Visitor.java`: Visitor 接口
- `<Grammar>BaseVisitor.java`: Visitor 默认实现
- `<Grammar>[Lexer].tokens`: 当语法被拆分成多个多个文件时用于同步编号

使用方法就是把 `*.java` 复制到项目中合适的位置，然后编写调用代码、Visitor及（或）Listener。