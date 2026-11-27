# Offline renderer for entry.png (run: python3 tools/build.py). Deterministic; main.ts ships the result.
from PIL import Image, ImageDraw, ImageFont
S = 2  # supersample
W = H = 1024
M = 40
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANSR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
img = Image.new("RGB", (W*S, H*S), "#f4efe4")
d = ImageDraw.Draw(img)
def F(p, s): return ImageFont.truetype(p, int(s*S))
def R(x0,y0,x1,y1,fill=None,outline=None,w=1): d.rectangle([x0*S,y0*S,x1*S,y1*S],fill=fill,outline=outline,width=w*S)
def P(pts,fill): d.polygon([(x*S,y*S) for x,y in pts],fill=fill)
def L(pts,fill,w): d.line([(x*S,y*S) for x,y in pts],fill=fill,width=int(w*S),joint="curve")
def E(x0,y0,x1,y1,fill=None,outline=None,w=1): d.ellipse([x0*S,y0*S,x1*S,y1*S],fill=fill,outline=outline,width=int(w*S))
def wrap(text, font, maxw):
    lines, cur = [], ""
    for wd in text.split():
        t = (cur+" "+wd).strip()
        if d.textlength(t, font=font) <= maxw*S: cur = t
        else: lines.append(cur); cur = wd
    lines.append(cur); return lines
def text(x, y, t, font, fill, maxw, lh=1.12, box_bottom=None):
    lines = wrap(t, font, maxw)
    for ln in lines:
        assert d.textlength(ln, font=font) <= maxw*S, ("overflow", ln)
        d.text((x*S, y*S), ln, font=font, fill=fill)
        y += font.size/S*lh
    if box_bottom: assert y <= box_bottom, ("text below box", t, y, box_bottom)
    return y

INK="#14181f"
# masthead
text(M, 34, "THE WORLD IN ONE DAY", F(SERIF,34), INK, 600)
d.text((W*S-M*S, 40*S), "FRIDAY 27 NOVEMBER 2026", font=F(SANS,19), fill="#7a1f1f", anchor="ra")
R(M,84,W-M,87,fill=INK)

# dominant panel
T,B = 100,520
R(M,T,W-M,B,fill="#0f2542")
TX = M+28; TW = 548
R(TX,T+26,TX+150,T+56,fill="#d62828")
d.text(((TX+75)*S,(T+41)*S),"TOP STORY",font=F(SANS,18),fill="#fff",anchor="mm")
R(TX+162,T+26,TX+162+262,T+56,fill="#f2c230")
d.text(((TX+162+131)*S,(T+41)*S),"ACCORDING TO TRUMP",font=F(SANS,18),fill="#0f2542",anchor="mm")
yh=text(TX,T+76,"Trump says Putin is open to a Ukraine deal",F(SERIF,48),"#ffffff",TW,lh=1.15,box_bottom=B-130)
R(TX,yh+14,TX+TW,yh+16,fill="#f2c230")
text(TX,yh+30,"Trump says he asked Putin to \u201cpull back\u201d military aggression across Europe. Kyiv warns Russia is readying a new mass strike.",F(SANSR,22),"#d6e0f0",TW,lh=1.25,box_bottom=B-12)
# right column: the quoted words, attributed (information, not decoration)
qx0,qx1 = 660, W-M-28
R(qx0,T+34,qx1,B-34,fill="#17335c")
R(qx0,T+34,qx0+8,B-34,fill="#f2c230")
d.text(((qx0+30)*S,(T+52)*S),"KYIV WARNS",font=F(SANS,22),fill="#f2c230")
text(qx0+30,T+130,"Russia is preparing a new mass strike in the coming days.",F(SERIF,30),"#ffffff",qx1-qx0-52,lh=1.2,box_bottom=B-110)
d.text(((qx0+30)*S,(B-92)*S),"VOLODYMYR ZELENSKY",font=F(SANS,19),fill="#f2c230")
d.text(((qx0+30)*S,(B-66)*S),"PRESIDENT OF UKRAINE",font=F(SANSR,16),fill="#cfd9ea")

# cards (no icons: type carries the story)
gap=20; cw=(W-2*M-gap)/2; top=B+gap; STRIP=62
ch=(H-M-STRIP-gap-top-gap)/2
cards=[
 ("UNITED STATES","#a84a12","Thanksgiving storm cuts power, disrupts flights","Gusts up to 70 mph hit the East Coast; hundreds of thousands lost power."),
 ("EUROPE","#1b6e5a","EU leaders wrestle over \u20ac1.6tn budget","The 2028\u201334 plan and Ukraine funding were debated at Thursday\u2019s summit."),
 ("TRADE","#6a3d9a","US tariff push targets 14 trading partners","Includes China, days after Xi\u2019s red-carpet welcome for Trump."),
 ("KOREA","#8a1c2b","North Korea pauses military aid to Russia","Per Ukrainian intelligence; a reported dispute over Moscow\u2019s remarks."),
]
for i,(k,col,hl,sub) in enumerate(cards):
    x0=M+(i%2)*(cw+gap); y0=top+(i//2)*(ch+gap); x1=x0+cw; y1=y0+ch
    R(x0,y0,x1,y1,fill="#ffffff",outline="#cfc8b8",w=2); R(x0,y0,x0+10,y1,fill=col)
    d.text(((x0+30)*S,(y0+12)*S),k,font=F(SANS,16),fill=col)
    yy=text(x0+30,y0+34,hl,F(SERIF,26),INK,cw-52,lh=1.15,box_bottom=y1-50)
    text(x0+30,yy+6,sub,F(SANSR,18),"#333",cw-52,lh=1.2,box_bottom=y1-6)
sy=H-M-STRIP
R(M,sy,W-M,H-M,fill=INK)
d.text(((M+22)*S,(sy+STRIP/2)*S),"ALSO",font=F(SANS,18),fill="#f2c230",anchor="lm")
for j,t in enumerate(["Bank of England to cut capital rules for UK-focused banks","Lithuania threatens Taiwan office status to mend China ties"]):
    assert d.textlength(t,font=F(SANS,19))<=(W-2*M-92-20)*S
    d.text(((M+92)*S,(sy+8+j*24)*S),t,font=F(SANS,19),fill="#ffffff")

# contrast audit (WCAG ratio) for every text/background pair used
def lum(h):
    h=h.lstrip("#"); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    la,lb=sorted((lum(a),lum(b)),reverse=True); return (la+0.05)/(lb+0.05)
PAIRS=[("#ffffff","#0f2542"),("#d6e0f0","#0f2542"),("#ffffff","#17335c"),("#f2c230","#17335c"),("#0f2542","#f2c230"),("#d6e0f0","#0f2542"),("#cfd9ea","#17335c"),
 ("#ffffff","#d62828"),("#333333","#ffffff"),(INK,"#ffffff"),("#1b6e5a","#ffffff"),("#a84a12","#ffffff"),("#6a3d9a","#ffffff"),
 ("#8a1c2b","#ffffff"),("#ffffff",INK),("#f2c230",INK),("#7a1f1f","#f4efe4"),(INK,"#f4efe4")]
for fg,bg in PAIRS: assert cr(fg,bg)>=4.5,("low contrast",fg,bg,cr(fg,bg))
img=img.resize((W,H),Image.LANCZOS)
img=img.quantize(colors=256,method=Image.MEDIANCUT,dither=Image.NONE)
img.save("entry.png",optimize=True)
