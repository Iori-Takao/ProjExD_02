import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),  #練習３　キー移動量　（縦、横）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:  
    """
    オブジェクトが画面内or画面外を判定し　真理値タプルを返す関数
    因数　ｒｃｔ：こうかとんｏｒ爆弾ＳＵｒｆａｃｅ　のｒｅｃｔ
    戻り値：横方向　縦方向はみ出し判定結果　（画面内：Ｔｒｕｅ　画面外：Ｆａｌｓｅ）
    """

    yoko, tate = True, True 
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False

    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  #練習３ コウカトンのSurfaceを抽出
    kk_rct.center = 900, 400

    bb_img = pg.Surface((20, 20))  #練習１ 透明のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #練習１ 赤い半径１０の円を作る
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()  #練習１ 爆弾Surfaceを抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  #練習２ 爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):  #練習５ コウカトンrectに爆弾rectが衝突したら
            print("Game Over")
            return 
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k, tpl in delta.items():  #練習３ keyとtupleをdeltaから抽出
            if key_lst[k]:  #練習３ キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)  #練習３ こうかとんを移動させる
        bb_rct.move_ip(vx, vy)  #練習２ 爆弾を移動させる

        yoko, tate = check_bound(bb_rct)
        if not yoko:  #横方向にはみ出たら
            vx *= -1

        if not tate:  #縦方向にはみ出たら
            vy *= -1

        bb_rct.move_ip(vx, vy)  #練習４ 移動量反転後　再び動かす

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()