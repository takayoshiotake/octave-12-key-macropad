// Bourns PEC12R-4x20F-Sxxxx
//
// This is a simplified model and details are omitted.

L = 20.0;
LB = 5.0;
F = 7.0;

color("gray") translate([0,0,6.1/2]) {
    cube([12.4,13.4,6.1], center=true);
    translate([0,0,6.1/2]) {
        cylinder(d=7, h=LB, $fn=36);
    };
    translate([0,0,6.1/2+LB]) {
        cylinder(d=6, h=L-6.1-LB-F, $fn=36);
        
        linear_extrude(F) {
            difference() {
                circle(d=6, $fn=36);
                translate([-3,-3]) {
                    square([6,1.5]);
                }
            }
        }
    }
}

color("silver") translate([0,0,-3.5]) {
    translate([-5/2,7]) {
        cylinder(d=1, h=3.5, $fn=36);
    }
    translate([5/2,7]) {
        cylinder(d=1, h=3.5, $fn=36);
    }
    translate([-5/2,-7.5]) {
        cylinder(d=1, h=3.5, $fn=36);
    }
    translate([0,-7.5]) {
        cylinder(d=1, h=3.5, $fn=36);
    }
    translate([5/2,-7.5]) {
        cylinder(d=1, h=3.5, $fn=36);
    }
    translate([-13.2/2,-2.1/2]) {
        cube([2.0,2.1,3.5]);
    }
    translate([13.2/2-2.0,-2.1/2]) {
        cube([2.0,2.1,3.5]);
    }
}
