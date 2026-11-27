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

# dominant panel: headline across the full width, then two attributed statements side by side
T,B = 100,520
R(M,T,W-M,B,fill="#0f2542")
TX = M+28; FW = W-2*M-56
R(TX,T+24,TX+150,T+54,fill="#d62828")
d.text(((TX+75)*S,(T+39)*S),"TOP STORY",font=F(SANS,18),fill="#fff",anchor="mm")
R(TX+162,T+24,TX+162+262,T+54,fill="#f2c230")
d.text(((TX+162+131)*S,(T+39)*S),"ACCORDING TO TRUMP",font=F(SANS,18),fill="#0f2542",anchor="mm")
yh=text(TX,T+68,"Trump says Putin is open to a Ukraine deal",F(SERIF,46),"#ffffff",FW,lh=1.12,box_bottom=T+190)
R(TX,yh+10,TX+FW,yh+12,fill="#f2c230")
bw=(FW-24)/2; by0=yh+28; by1=B-28
for k,(who,role,quote) in enumerate([
  ("TRUMP SAYS","US PRESIDENT","Putin is ready for a deal. He urged Russia to \u201cpull back\u201d in Europe."),
  ("ZELENSKY SAYS","PRESIDENT OF UKRAINE","Russia is preparing a new mass strike in the coming days.")]):
    bx=TX+k*(bw+24)
    R(bx,by0,bx+bw,by1,fill="#17335c"); R(bx,by0,bx+8,by1,fill="#f2c230")
    d.text(((bx+28)*S,(by0+12)*S),who,font=F(SANS,21),fill="#f2c230")
    text(bx+28,by0+42,quote,F(SERIF,26),"#ffffff",bw-48,lh=1.2,box_bottom=by1-8)

# cards: a big figure anchors each story (type carries it, no icons)
gap=20; cw=(W-2*M-gap)/2; top=B+gap; STRIP=62
ch=(H-M-STRIP-gap-top-gap)/2
cards=[
 ("70 mph","UNITED STATES","#a84a12","Thanksgiving storm cuts power, grounds flights","Hundreds of thousands lost power."),
 ("\u20ac1.6tn","EUROPE","#1b6e5a","EU leaders wrestle over 2028\u201334 budget","Ukraine funding was also on the table."),
 ("14","TRADE","#6a3d9a","US tariff push targets 14 trading partners","China is among them."),
 ("PAUSED","KOREA","#8a1c2b","North Korea halts military aid to Russia","Per Ukrainian intelligence."),
]
for i,(big,k,col,hl,sub) in enumerate(cards):
    x0=M+(i%2)*(cw+gap); y0=top+(i//2)*(ch+gap); x1=x0+cw; y1=y0+ch
    R(x0,y0,x1,y1,fill="#ffffff",outline="#cfc8b8",w=2); R(x0,y0,x0+10,y1,fill=col)
    d.text(((x0+30)*S,(y0+8)*S),big,font=F(SERIF,40),fill=col)
    d.text(((x1-20)*S,(y0+30)*S),k,font=F(SANS,18),fill=col,anchor="ra")
    yy=text(x0+30,y0+62,hl,F(SERIF,25),INK,cw-52,lh=1.15,box_bottom=y1-34)
    text(x0+30,yy+4,sub,F(SANSR,20),"#333",cw-52,lh=1.2,box_bottom=y1-6)
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
