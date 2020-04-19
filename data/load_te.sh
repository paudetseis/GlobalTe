gmt xyz2grd te_global.1deg.xyz -Gte_global.1deg.grd -Rd -I2 -rp -V
# gmt grdedit te_global.1deg.grd -T -V
gmt grd2xyz te_global.1deg.grd > te_global.xyz
