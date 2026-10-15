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
    'preference-harness': ('人手持红色弧形栏杆选择喜爱的桥型，机械伙伴用砝码检验承重；红桥下弯，旁边带三角支撑的青桥保持平直。', 'A person favors a red curved railing while a mechanical counterpart tests load-bearing support with weights; the red bridge sags beside a level, triangulated teal bridge.'),
    'finite-inquiry-and-abstraction': ('溪流中的取样框与稀疏的托盘模型保留相关关系，让有限表示回答具体问题。', 'A creek sampling frame and a sparse tray model preserve relevant relations for a question within finite means.'),
    'yinyang-and-taiji': ('日月下的黑白双鱼在陶碗中相绕游动，幼芽的根扎进可见的土壤，把生成带入物质世界。', 'Black and white fish circle in an earthen bowl beneath Sun and Moon; a sprout’s visible roots enter the soil, bringing generation into the material world.'),
    'participation-and-support': ('一人自己选择过河的踏脚石，同伴把下一块石头放到可及之处。', 'A person chooses their own stepping stone while a companion places another within reach.'),
    'literary-programming': ('书中的火焰人物展开为灯、积木桥与收纳托盘，人与月形伙伴把凝缩的意象用于共同实践。', 'A flame character in a book unfolds into a lamp, block bridge, and organizing tray, as a person and moonlike counterpart put condensed imagery into practice.'),
    'metaphor-and-self-revision': ('人与陶土伙伴对照积木模型、草图和实际拱桥，一起调整不合适的弧形部件，让制作中的发现修订共同模型。', 'A person and clay companion compare a block model, sketch, and working arch, adjusting a curved piece so discoveries in making revise their shared model.'),
    'writing-a-sinthome': ('人与伙伴编织三色绳索，调整托住笔记本、幼苗杯与灯笼的环，让个人实践形成可维系生活与创造的结构。', 'A person and companion weave a three-color cord, adjusting loops around a notebook, sprout cup, and lantern into a sustaining form for living and creating.'),
    'local-source-and-website': ('同一工作台上的四面体连接透镜、心形石与扳手三个支点，表示哲学、心理与工程在共同物理现实中的不同层次。', 'A tetrahedral structure on one workbench connects a lens, heart stone, and wrench, expressing philosophy, psychology, and engineering as distinct levels within shared physical reality.'),
    'embodied-experimental-philosophy': ('斜坡上的滚动物体挑战纸上的计划，试作者根据实际结果重新绘制安排。', 'A rolling object on a ramp challenges a paper plan, prompting the experimenter to redraw the arrangement through its actual consequences.'),
    'example-and-commons': ('三位朋友打开同一工具包，分别制作风筝、木偶与乐器，让共享资源形成不同创造。', 'Three friends open a shared toolkit and make a kite, puppet, and musical object, developing common resources into distinct creations.'),
    'lacan-and-description-logic': ('说话者把相连的彩色形状放入笔记本中的未完成自画像，另一只手仍握着画面没有容纳的星形。', 'A speaker places linked colored shapes into an unfinished notebook self-portrait while holding a star absent from that account.'),
    'deleuze-and-becoming': ('吹笛的人、纸喇叭与捧碗的伙伴通过彩色声流连接，交汇的声音生成一只新的飞鸟。', 'A flute player, paper horn, and bowl-holding companion connect through colored sound currents that compose a new flying bird.'),
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
    if not (dist / 'art' / f'{name}.png').is_file():
        return ''
    alt = html.escape(scene_alt(name, chinese), quote=True)
    inset = time_inset(chinese) if name == 'flow-and-time' else ''
    return f'<figure class="article-art"><img src="/art/{name}.png" alt="{alt}" width="1536" height="1024" fetchpriority="high">{inset}</figure>'
