"""Shared scene descriptions and artwork markup for both essay renderers."""
import html


# Describe the depicted relation, rather than repeating the essay's title.
SCENES = {
    'stealing-fire': ('一人从共享熔炉借来微小火种，亲手照料自己的炉火，把借来的能力发展为自己的创造。', 'A person borrows a tiny ember from a shared furnace and tends their own hearth, developing borrowed capability into creation.'),
    'personal-first-humanism': ('一人主动塑造陶鸟，机械伙伴调整灯光、可及的托盘与工作台，让工具适合这个人的身体与创作。', 'A person shapes a clay bird while a robotic counterpart adjusts a lamp, reachable tray, and workbench to fit their body and creation.'),
    'why-yinyang': ('人与伙伴分别为同一悬挂作品添加不同部件，探究、写作与制作工具围绕共同方向连接起来。', 'A person and counterpart add different components to one hanging mobile, connecting inquiry, writing, and making around a shared direction.'),
    'meng': ('好奇的小狮子在引导下尝试玩具难题，以开放与共同学习发展能力。', 'A curious lion cub tries a toy puzzle with guidance, developing through openness and shared learning.'),
    'baby-heraclitus': ('火焰孩子在河边塑造陶土，在接触材料与流动世界时继续形成自己。', 'A child of flame shapes clay beside a river, becoming through contact with materials and a changing world.'),
    'world-and-expression': ('真实的柑橘树立在可修订的写生旁，树的细节促使画面改变。', 'A living citrus tree stands beside a revisable sketch; details of the tree prompt changes in its representation.'),
    'flow-and-time': ('两条并行水流节奏不同，人与月形伙伴把上游卵石留在记忆篮中，并用新的相遇继续搭桥。', 'Two parallel currents flow at different rhythms; a person and moonlike counterpart retain upstream pebbles in a memory basket while building a bridge through new encounters.'),
    'reasoning': ('尚未完成的分岔弹珠轨道正在组装，候选路线等待实际滚动来检验。', 'An unfinished branching marble run is being assembled, with possible routes awaiting a trial to test their consequences.'),
    'preference-harness': ('人用爱心选中房子到风车之间的红色林荫路线，机械伙伴对照桥梁报告检查过河的连接；下方另有一条候选路线。', 'A person marks a red tree-lined route from house to windmill with a heart, while a mechanical counterpart checks its river crossing against a bridge report; another candidate runs below.'),
    'finite-inquiry-and-abstraction': ('细致小镇与右侧简图保留相同的房子、风车、河流、桥梁和连通道路；手指对照两处桥梁，简图略去了花草、瓦片与石头。', 'A detailed town and its simple map retain the same house, windmill, river, bridge, and connected road; fingers compare the bridges while the map omits flowers, roof tiles, and stones.'),
    'yinyang-and-taiji': ('一黑一白两条鱼首尾相承，围绕留白相绕游动；黑鱼白眼，白鱼黑眼。', 'One black fish and one white fish circle head-to-tail around an open center, each with a contrasting eye.'),
    'participation-and-support': ('一人自己选择过河的踏脚石，同伴把下一块石头放到可及之处。', 'A person chooses their own stepping stone while a companion places another within reach.'),
    'literary-programming': ('书中的火焰人物展开为灯、积木桥与收纳托盘，人与月形伙伴把凝缩的意象用于共同实践。', 'A flame character in a book unfolds into a lamp, block bridge, and organizing tray, as a person and moonlike counterpart put condensed imagery into practice.'),
    'metaphor-and-self-revision': ('人与陶土伙伴对照积木模型、草图和实际拱桥，一起调整不合适的弧形部件，让制作中的发现修订共同模型。', 'A person and clay companion compare a block model, sketch, and working arch, adjusting a curved piece so discoveries in making revise their shared model.'),
    'writing-a-sinthome': ('左侧博罗米结的青、红、赭三个闭环共同套连，交叉处标明上下穿越；右侧去掉红环，余下的青环与赭环可以分开。', 'At left, teal, vermilion, and ochre Borromean rings hold together with explicit over-and-under crossings; at right, removal of the vermilion ring lets the teal and ochre rings separate.'),
    'local-source-and-website': ('同一工作台上的四面体连接透镜、心形石与扳手三个支点，表示哲学、心理与工程在共同物理现实中相互影响。', 'A tetrahedral structure on one workbench connects a lens, heart stone, and wrench, expressing how philosophy, psychology, and engineering affect one another within shared physical reality.'),
    'embodied-experimental-philosophy': ('斜坡上的滚动物体挑战纸上的计划，试作者根据实际结果重新绘制安排。', 'A rolling object on a ramp challenges a paper plan, prompting the experimenter to redraw the arrangement through its actual consequences.'),
    'example-and-commons': ('三位朋友打开同一工具包，分别制作风筝、木偶与乐器，让共享资源形成不同创造。', 'Three friends open a shared toolkit and make a kite, puppet, and musical object, developing common resources into distinct creations.'),
    'speech-opposition-and-self-formation': ('说话者把相连的彩色形状放入笔记本中的未完成自画像，另一只手仍握着画面没有容纳的星形。', 'A speaker places linked colored shapes into an unfinished notebook self-portrait while holding a star absent from that account.'),
    'deleuze-and-becoming': ('吹笛的人、纸喇叭与捧碗的伙伴通过彩色声流连接，交汇的声音生成一只新的飞鸟。', 'A flute player, paper horn, and bowl-holding companion connect through colored sound currents that compose a new flying bird.'),
}

CAPTIONS = {
    'preference-harness': ('爱心选方向，报告供检查：想走林荫路，还要确认桥能通过。', 'The heart selects a direction; the report supports a check: a preferred shaded route still needs a passable bridge.'),
    'finite-inquiry-and-abstraction': ('从房子到风车：简图保留道路与桥的连接，略去不影响这次寻路的细节。', 'From house to windmill: the map preserves road and bridge connections while omitting detail irrelevant to this route.'),
    'writing-a-sinthome': ('博罗米结的三环联结示意：去掉红环，另外两个便能分开。这幅图说明联结性质；正文另行展开个人实践安排的形成与表示。', 'A three-ring Borromean link: remove the vermilion ring and the other two can separate. This figure illustrates linkage; the text separately develops the formation and representation of a personal practice arrangement.'),
}


def scene_alt(name, chinese):
    return SCENES[name][0 if chinese else 1]


def time_inset(chinese):
    """A single finite transition: occurrence, retained trace, revised account."""
    labels = ('外界变化', '当前理解', '旧迹保留，新相遇进入现在。') if chinese else ('World changes', 'Account updates', 'Earlier traces remain as a new encounter changes the present.')
    description = ('两股水流以不同速度到达：外界先变，当前理解随后修订；早先相遇的虚线圆环仍然保留。动画在4.8秒后停止。' if chinese else 'Two currents arrive at different speeds: the world changes first, then the working account updates. A dashed ring retains the earlier encounter. The animation ends after 4.8 seconds.')
    return f'''<div class="time-inset"><svg viewBox="0 0 340 112" role="img" aria-label="{description}">
<text x="8" y="23">{labels[0]}</text><text x="8" y="75">{labels[1]}</text>
<path class="time-current" d="M116 20 Q174 4 225 26 T319 21 M116 72 Q174 56 225 78 T319 73"/>
<path class="time-retained" d="M132 20 Q177 8 220 25"/>
<circle class="time-old" cx="220" cy="73" r="10"/>
<circle class="time-event time-event-world" cx="124" cy="20" r="4"/>
<circle class="time-event time-event-account" cx="124" cy="72" r="4"/>
<circle class="time-trace" cx="220" cy="25" r="5"/>
<circle class="time-new" cx="292" cy="73" r="13"/>
<path class="time-integration" d="M230 73 Q260 53 279 73"/>
</svg><p class="time-caption">{labels[2]}</p><button class="time-replay" type="button">{'重播变化' if chinese else 'Replay change'}</button></div><script src="/article-art.js" defer></script>'''


def article_figure(dist, name, chinese):
    extension = 'svg' if name == 'writing-a-sinthome' else 'png'
    if not (dist / 'art' / f'{name}.{extension}').is_file():
        return ''
    alt = html.escape(scene_alt(name, chinese), quote=True)
    inset = time_inset(chinese) if name == 'flow-and-time' else ''
    caption = f'<figcaption>{html.escape(CAPTIONS[name][0 if chinese else 1])}</figcaption>' if name in CAPTIONS else ''
    return f'<figure class="article-art"><img src="/art/{name}.{extension}" alt="{alt}" width="1536" height="1024" fetchpriority="high">{caption}{inset}</figure>'
