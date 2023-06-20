grammar graphQL;
program: (stmt SMCLN)* EOF;

stmt: print_expr | assign;

print_expr: PRINT LP expr RP;
assign: var ASSIGN expr;
var: NAME;

expr:
    LP expr RP
    | var           // переменные
    | val           // константы
    | vertex        // вершина
    | vertices      // набор вершин
    | edge          // ребро
    | edges         // набор рёбер
    | map_expr      // классический map
    | labels        // метки (напр. когда их необходимо получить)
    | filter_expr   // классический filter
    | graph         // граф (вручную или загруженный)
    | intersection  // пересечение языков
    | concatenation // конкатенация языков
    | union         // объединение языков
    | star          // замыкание языков (звезда Клини)
    | equality;     // проверка равенства

boolean:   'True' | 'False';
val:    boolean | INT | STR;
label:  var | INT | STR;                                  // TODO: мне бы хотелось обходиться со всеми лейблами как со строками (а лучше даже отдельными терминалами или нетерминалами)

lambda_expr: LAMBDA (var CM)* (var)? ARR expr;      // допустима лямбда нулевой арности
map_expr:    MAP LP lambda_expr CM expr RP;
filter_expr: FILTER LP lambda_expr CM expr RP;

vertex: var | INT;
edge:   var | LP vertex ',' label ',' vertex RP;

vertices:
    LB (vertex CM)* (vertex)? RB
    | GET_START     LP graph RP         // получить множество стартовых состояний
    | GET_FINAL     LP graph RP         // получить множество финальных состояний
    | GET_REACHABLE LP graph RP         // получить все пары достижимых вершин TODO: если пары, то это не vertices, а их пары... ну ладно, глянем
    | GET_VERTICES  LP graph RP;        // получить все вершины

edges:
    LB (edge CM)* (edge)? RB
    | GET_EDGES LP graph RP;    // получить все рёбра

labels:
    LB (label CM)* (label)? RB
    | GET_LABELS LP graph RP;   // получить все метки

graph:
    SET_START LP vertices CM graph RP   // задать множество стартовых состояний
    | SET_FINAL LP vertices CM graph RP // задать множество финальных состояний
    | ADD_START LP vertices CM graph RP // добавить состояния в множество стартовых
    | ADD_FINAL LP vertices CM graph RP // добавить состояния в множество финальных
    | LOAD_GRAPH LP STR RP;             // загрузка графа

intersection:   INTERSECT LP expr CM expr RP;
concatenation:  CONCAT LP expr CM expr RP;
union:          UNITE LP expr CM expr RP;
star:           STAR LP expr RP;
equality:       LP expr EQUAL expr RP;


//  | Smb of expr TODO: "единичный переход" - чего?

CM:     ',';
SMCLN:  ';';
LP:     '(';
RP:     ')';
LB:     '{';
RB:     '}';
ASSIGN: '=';
EQUAL:  '==';
ARR:    '->';

PRINT:  'print';
LAMBDA: 'lambda';
MAP:    'map';
FILTER: 'filter';


GET_START:      'get_start';
GET_FINAL:      'get_final';
GET_REACHABLE:  'get_reachable';
GET_VERTICES:   'get_vertices';
GET_EDGES:      'get_edges';
GET_LABELS:     'get_labels';

SET_START:      'set_start';
SET_FINAL:      'set_final';

ADD_START:      'add_start';
ADD_FINAL:      'add_final';

LOAD_GRAPH:     'load_graph';

INTERSECT:      'intersect';
CONCAT:         'concat';
UNITE:          'unite';
STAR:           'star';

NAME: [_a-zA-Z][_a-zA-Z0-9]* ;
INT: '-'? [1-9] [0-9]* | '0';
STR: '"' .*? '"' ;
