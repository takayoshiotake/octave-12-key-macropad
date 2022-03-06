// Hot swap socket
//
// This designed so that the center pin of MX compatible keyboard switches is centered.
// Also, this is a simplified model and details are omitted.

cx = (1.27*3 - 1.27*2)/2;
cy = 1.27*3;

color("beige") translate([0,0,0.05]) {
    linear_extrude(1.80) {
        difference() {
            translate([cx,cy]) {
                square(size=[10.90,5.89], center=true);
            }
            
            gap = 5.89 - 4;
            translate([cx-10.90/2,cy-(5.89/2)]) {
                square(size=[10.90/2-cx,gap]);
            }

            // Calculate from the center pin of the key switch
            circle(r=cy-(5.89/2)+gap, $fn=36);
        }
    }

    translate([-1.27*2,1.27*4,-(3.05-1.80)]) {
        // d±0.05
        cylinder(d=2.9, h=3.05-1.80, $fn=36);
    }
    
    translate([1.27*3,1.27*2,-(3.05-1.80)]) {
        // d±0.05
        cylinder(d=2.9, h=3.05-1.80, $fn=36);
    }
}

color("silver") linear_extrude(1.85) {
    //pad_min_margin = 11.30;
    pad_min_margin = 10.90;
    pad_len = (14.50 - pad_min_margin)/2;
    
    translate([cx-pad_min_margin/2-pad_len/2,1.27*4]) {
        square([pad_len,1.68], center=true);
    }
    
    translate([cx+pad_min_margin/2+pad_len/2,1.27*2]) {
        square([pad_len,1.68], center=true);
    }
}
