(G-CODE GENERATED BY FLATCAM v8.994 - www.flatcam.org - Version Date: 2020/11/7)

(Name: Gerber_BoardOutline.GKO_cutout_cnc)
(Type: G-code from Geometry)
(Units: MM)

(Created on Thursday, 04 March 2021 at 11:46)

(This preprocessor is the default preprocessor used by FlatCAM.)
(It is made to work with MACH3 compatible motion controllers.)

(TOOL DIAMETER: 2.4 mm)
(Feedrate_XY: 120.0 mm/min)
(Feedrate_Z: 60.0 mm/min)
(Feedrate rapids 1500.0 mm/min)

(Z_Cut: -1.8 mm)
(DepthPerCut: 0.6 mm <=>3 passes)
(Z_Move: 2.0 mm)
(Z Start: None mm)
(Z End: 15.0 mm)
(X,Y End: None mm)
(Steps per circle: 64)
(Preprocessor Geometry: default)

(X range:   -1.4271 ...   86.4957  mm)
(Y range:   -1.3700 ...   51.3665  mm)

(Spindle Speed: 0.0 RPM)
G21
G90
G94

G01 F120.00

M5
G00 Z15.0000
G00 X0.0000 Y0.0000
T1
M6    
(MSG, Change to Tool Dia = 2.4000)
M0
G00 Z15.0000

M03
G01 F120.00
G00 X-1.4271 Y21.9286
G01 F60.00
G01 Z-0.6000
G01 F120.00
G01 X-1.4271 Y0.0581
G01 X-1.4255 Y-0.0067
G01 X-1.4249 Y-0.0191
G01 X-1.4124 Y-0.1461
G01 X-1.4106 Y-0.1584
G01 X-1.3857 Y-0.2836
G01 X-1.3826 Y-0.2957
G01 X-1.3456 Y-0.4177
G01 X-1.3414 Y-0.4295
G01 X-1.2926 Y-0.5473
G01 X-1.2872 Y-0.5586
G01 X-1.2271 Y-0.6711
G01 X-1.2207 Y-0.6818
G01 X-1.1498 Y-0.7879
G01 X-1.1424 Y-0.7979
G01 X-1.0615 Y-0.8965
G01 X-1.0531 Y-0.9058
G01 X-0.9629 Y-0.9960
G01 X-0.9536 Y-1.0044
G01 X-0.8550 Y-1.0853
G01 X-0.8450 Y-1.0927
G01 X-0.7389 Y-1.1636
G01 X-0.7282 Y-1.1700
G01 X-0.6157 Y-1.2301
G01 X-0.6044 Y-1.2355
G01 X-0.4866 Y-1.2843
G01 X-0.4748 Y-1.2885
G01 X-0.3528 Y-1.3255
G01 X-0.3407 Y-1.3286
G01 X-0.2155 Y-1.3534
G01 X-0.2032 Y-1.3553
G01 X-0.0762 Y-1.3678
G01 X-0.0638 Y-1.3684
G01 X0.0000 Y-1.3700
G01 X39.4450 Y-1.3700
G00 X39.4450 Y-1.3700
G01 F60.00
G01 Z-1.2000
G01 F120.00
G01 X0.0000 Y-1.3700
G01 X-0.0638 Y-1.3684
G01 X-0.0762 Y-1.3678
G01 X-0.2032 Y-1.3553
G01 X-0.2155 Y-1.3534
G01 X-0.3407 Y-1.3286
G01 X-0.3528 Y-1.3255
G01 X-0.4748 Y-1.2885
G01 X-0.4866 Y-1.2843
G01 X-0.6044 Y-1.2355
G01 X-0.6157 Y-1.2301
G01 X-0.7282 Y-1.1700
G01 X-0.7389 Y-1.1636
G01 X-0.8450 Y-1.0927
G01 X-0.8550 Y-1.0853
G01 X-0.9536 Y-1.0044
G01 X-0.9629 Y-0.9960
G01 X-1.0531 Y-0.9058
G01 X-1.0615 Y-0.8965
G01 X-1.1424 Y-0.7979
G01 X-1.1498 Y-0.7879
G01 X-1.2207 Y-0.6818
G01 X-1.2271 Y-0.6711
G01 X-1.2872 Y-0.5586
G01 X-1.2926 Y-0.5473
G01 X-1.3414 Y-0.4295
G01 X-1.3456 Y-0.4177
G01 X-1.3826 Y-0.2957
G01 X-1.3857 Y-0.2836
G01 X-1.4106 Y-0.1584
G01 X-1.4124 Y-0.1461
G01 X-1.4249 Y-0.0191
G01 X-1.4255 Y-0.0067
G01 X-1.4271 Y0.0581
G01 X-1.4271 Y21.9286
G00 X-1.4271 Y21.9286
G01 F60.00
G01 Z-1.8000
G01 F120.00
G01 X-1.4271 Y0.0581
G01 X-1.4255 Y-0.0067
G01 X-1.4249 Y-0.0191
G01 X-1.4124 Y-0.1461
G01 X-1.4106 Y-0.1584
G01 X-1.3857 Y-0.2836
G01 X-1.3826 Y-0.2957
G01 X-1.3456 Y-0.4177
G01 X-1.3414 Y-0.4295
G01 X-1.2926 Y-0.5473
G01 X-1.2872 Y-0.5586
G01 X-1.2271 Y-0.6711
G01 X-1.2207 Y-0.6818
G01 X-1.1498 Y-0.7879
G01 X-1.1424 Y-0.7979
G01 X-1.0615 Y-0.8965
G01 X-1.0531 Y-0.9058
G01 X-0.9629 Y-0.9960
G01 X-0.9536 Y-1.0044
G01 X-0.8550 Y-1.0853
G01 X-0.8450 Y-1.0927
G01 X-0.7389 Y-1.1636
G01 X-0.7282 Y-1.1700
G01 X-0.6157 Y-1.2301
G01 X-0.6044 Y-1.2355
G01 X-0.4866 Y-1.2843
G01 X-0.4748 Y-1.2885
G01 X-0.3528 Y-1.3255
G01 X-0.3407 Y-1.3286
G01 X-0.2155 Y-1.3534
G01 X-0.2032 Y-1.3553
G01 X-0.0762 Y-1.3678
G01 X-0.0638 Y-1.3684
G01 X0.0000 Y-1.3700
G01 X39.4450 Y-1.3700
G00 Z2.0000
G00 X-0.3734 Y28.3286
G01 F60.00
G01 Z-0.6000
G01 F120.00
G01 X1.6129 Y31.2090
G01 X1.6573 Y31.2697
G01 X1.6967 Y31.3187
G01 X4.8142 Y35.0166
G01 X4.8559 Y35.0637
G01 X4.9082 Y35.1177
G01 X8.3685 Y38.4971
G01 X8.4146 Y38.5399
G01 X8.4718 Y38.5886
G01 X12.2425 Y41.6178
G01 X12.2924 Y41.6560
G01 X12.3541 Y41.6990
G01 X16.3998 Y44.3497
G01 X16.4638 Y44.3891
G01 X16.5188 Y44.4197
G01 X20.8016 Y46.6671
G01 X20.8692 Y46.7001
G01 X20.9268 Y46.7253
G01 X25.4068 Y48.5483
G01 X25.4656 Y48.5706
G01 X25.5370 Y48.5941
G01 X30.1722 Y49.9758
G01 X30.2329 Y49.9923
G01 X30.3062 Y50.0088
G01 X35.0532 Y50.9362
G01 X35.1152 Y50.9468
G01 X35.1898 Y50.9561
G01 X39.4450 Y51.3665
G00 X39.4450 Y51.3665
G01 F60.00
G01 Z-1.2000
G01 F120.00
G01 X35.1898 Y50.9561
G01 X35.1152 Y50.9468
G01 X35.0532 Y50.9362
G01 X30.3062 Y50.0088
G01 X30.2329 Y49.9923
G01 X30.1722 Y49.9758
G01 X25.5370 Y48.5941
G01 X25.4656 Y48.5706
G01 X25.4068 Y48.5483
G01 X20.9268 Y46.7253
G01 X20.8692 Y46.7001
G01 X20.8016 Y46.6671
G01 X16.5188 Y44.4197
G01 X16.4638 Y44.3891
G01 X16.3998 Y44.3497
G01 X12.3541 Y41.6990
G01 X12.2924 Y41.6560
G01 X12.2425 Y41.6178
G01 X8.4718 Y38.5886
G01 X8.4146 Y38.5399
G01 X8.3685 Y38.4971
G01 X4.9082 Y35.1177
G01 X4.8559 Y35.0637
G01 X4.8142 Y35.0166
G01 X1.6967 Y31.3187
G01 X1.6573 Y31.2697
G01 X1.6129 Y31.2090
G01 X-0.3734 Y28.3286
G00 X-0.3734 Y28.3286
G01 F60.00
G01 Z-1.8000
G01 F120.00
G01 X1.6129 Y31.2090
G01 X1.6573 Y31.2697
G01 X1.6967 Y31.3187
G01 X4.8142 Y35.0166
G01 X4.8559 Y35.0637
G01 X4.9082 Y35.1177
G01 X8.3685 Y38.4971
G01 X8.4146 Y38.5399
G01 X8.4718 Y38.5886
G01 X12.2425 Y41.6178
G01 X12.2924 Y41.6560
G01 X12.3541 Y41.6990
G01 X16.3998 Y44.3497
G01 X16.4638 Y44.3891
G01 X16.5188 Y44.4197
G01 X20.8016 Y46.6671
G01 X20.8692 Y46.7001
G01 X20.9268 Y46.7253
G01 X25.4068 Y48.5483
G01 X25.4656 Y48.5706
G01 X25.5370 Y48.5941
G01 X30.1722 Y49.9758
G01 X30.2329 Y49.9923
G01 X30.3062 Y50.0088
G01 X35.0532 Y50.9362
G01 X35.1152 Y50.9468
G01 X35.1898 Y50.9561
G01 X39.4450 Y51.3665
G00 Z2.0000
G00 X45.8450 Y51.3462
G01 F60.00
G01 Z-0.6000
G01 F120.00
G01 X49.9304 Y50.9471
G01 X50.0050 Y50.9377
G01 X50.0670 Y50.9270
G01 X54.8128 Y49.9939
G01 X54.8742 Y49.9802
G01 X54.9468 Y49.9607
G01 X59.5802 Y48.5733
G01 X59.6400 Y48.5539
G01 X59.7104 Y48.5274
G01 X64.1881 Y46.6988
G01 X64.2458 Y46.6737
G01 X64.3133 Y46.6405
G01 X68.5934 Y44.3879
G01 X68.6483 Y44.3573
G01 X68.7123 Y44.3178
G01 X72.7547 Y41.6621
G01 X72.8164 Y41.6191
G01 X72.8663 Y41.5808
G01 X76.6332 Y38.5470
G01 X76.6812 Y38.5064
G01 X76.7364 Y38.4553
G01 X80.1926 Y35.0718
G01 X80.2364 Y35.0267
G01 X80.2864 Y34.9705
G01 X83.3995 Y31.2689
G01 X83.4388 Y31.2197
G01 X83.4795 Y31.1642
G01 X85.4501 Y28.3286
G00 X85.4501 Y28.3286
G01 F60.00
G01 Z-1.2000
G01 F120.00
G01 X83.4795 Y31.1642
G01 X83.4388 Y31.2197
G01 X83.3995 Y31.2689
G01 X80.2864 Y34.9705
G01 X80.2364 Y35.0267
G01 X80.1926 Y35.0718
G01 X76.7364 Y38.4553
G01 X76.6812 Y38.5064
G01 X76.6332 Y38.5470
G01 X72.8663 Y41.5808
G01 X72.8164 Y41.6191
G01 X72.7547 Y41.6621
G01 X68.7123 Y44.3178
G01 X68.6483 Y44.3573
G01 X68.5934 Y44.3879
G01 X64.3133 Y46.6405
G01 X64.2458 Y46.6737
G01 X64.1881 Y46.6988
G01 X59.7104 Y48.5274
G01 X59.6400 Y48.5539
G01 X59.5802 Y48.5733
G01 X54.9468 Y49.9607
G01 X54.8742 Y49.9802
G01 X54.8128 Y49.9939
G01 X50.0670 Y50.9270
G01 X50.0050 Y50.9377
G01 X49.9304 Y50.9471
G01 X45.8450 Y51.3462
G00 X45.8450 Y51.3462
G01 F60.00
G01 Z-1.8000
G01 F120.00
G01 X49.9304 Y50.9471
G01 X50.0050 Y50.9377
G01 X50.0670 Y50.9270
G01 X54.8128 Y49.9939
G01 X54.8742 Y49.9802
G01 X54.9468 Y49.9607
G01 X59.5802 Y48.5733
G01 X59.6400 Y48.5539
G01 X59.7104 Y48.5274
G01 X64.1881 Y46.6988
G01 X64.2458 Y46.6737
G01 X64.3133 Y46.6405
G01 X68.5934 Y44.3879
G01 X68.6483 Y44.3573
G01 X68.7123 Y44.3178
G01 X72.7547 Y41.6621
G01 X72.8164 Y41.6191
G01 X72.8663 Y41.5808
G01 X76.6332 Y38.5470
G01 X76.6812 Y38.5064
G01 X76.7364 Y38.4553
G01 X80.1926 Y35.0718
G01 X80.2364 Y35.0267
G01 X80.2864 Y34.9705
G01 X83.3995 Y31.2689
G01 X83.4388 Y31.2197
G01 X83.4795 Y31.1642
G01 X85.4501 Y28.3286
G00 Z2.0000
G00 X86.4957 Y21.9286
G01 F60.00
G01 Z-0.6000
G01 F120.00
G01 X86.3900 Y0.0502
G01 X86.3882 Y-0.0134
G01 X86.3875 Y-0.0258
G01 X86.3745 Y-0.1523
G01 X86.3726 Y-0.1646
G01 X86.3473 Y-0.2892
G01 X86.3442 Y-0.3013
G01 X86.3068 Y-0.4228
G01 X86.3026 Y-0.4345
G01 X86.2535 Y-0.5518
G01 X86.2481 Y-0.5631
G01 X86.1878 Y-0.6750
G01 X86.1814 Y-0.6857
G01 X86.1104 Y-0.7912
G01 X86.1029 Y-0.8012
G01 X86.0220 Y-0.8993
G01 X86.0136 Y-0.9085
G01 X85.9235 Y-0.9982
G01 X85.9142 Y-1.0065
G01 X85.8158 Y-1.0870
G01 X85.8058 Y-1.0944
G01 X85.6999 Y-1.1648
G01 X85.6892 Y-1.1712
G01 X85.5770 Y-1.2310
G01 X85.5657 Y-1.2363
G01 X85.4481 Y-1.2848
G01 X85.4364 Y-1.2890
G01 X85.3147 Y-1.3258
G01 X85.3026 Y-1.3288
G01 X85.1779 Y-1.3535
G01 X85.1656 Y-1.3554
G01 X85.0390 Y-1.3678
G01 X85.0266 Y-1.3684
G01 X84.9630 Y-1.3700
G01 X45.8450 Y-1.3700
G00 X45.8450 Y-1.3700
G01 F60.00
G01 Z-1.2000
G01 F120.00
G01 X84.9630 Y-1.3700
G01 X85.0266 Y-1.3684
G01 X85.0390 Y-1.3678
G01 X85.1656 Y-1.3554
G01 X85.1779 Y-1.3535
G01 X85.3026 Y-1.3288
G01 X85.3147 Y-1.3258
G01 X85.4364 Y-1.2890
G01 X85.4481 Y-1.2848
G01 X85.5657 Y-1.2363
G01 X85.5770 Y-1.2310
G01 X85.6892 Y-1.1712
G01 X85.6999 Y-1.1648
G01 X85.8058 Y-1.0944
G01 X85.8158 Y-1.0870
G01 X85.9142 Y-1.0065
G01 X85.9235 Y-0.9982
G01 X86.0136 Y-0.9085
G01 X86.0220 Y-0.8993
G01 X86.1029 Y-0.8012
G01 X86.1104 Y-0.7912
G01 X86.1814 Y-0.6857
G01 X86.1878 Y-0.6750
G01 X86.2481 Y-0.5631
G01 X86.2535 Y-0.5518
G01 X86.3026 Y-0.4345
G01 X86.3068 Y-0.4228
G01 X86.3442 Y-0.3013
G01 X86.3473 Y-0.2892
G01 X86.3726 Y-0.1646
G01 X86.3745 Y-0.1523
G01 X86.3875 Y-0.0258
G01 X86.3882 Y-0.0134
G01 X86.3900 Y0.0502
G01 X86.4957 Y21.9286
G00 X86.4957 Y21.9286
G01 F60.00
G01 Z-1.8000
G01 F120.00
G01 X86.3900 Y0.0502
G01 X86.3882 Y-0.0134
G01 X86.3875 Y-0.0258
G01 X86.3745 Y-0.1523
G01 X86.3726 Y-0.1646
G01 X86.3473 Y-0.2892
G01 X86.3442 Y-0.3013
G01 X86.3068 Y-0.4228
G01 X86.3026 Y-0.4345
G01 X86.2535 Y-0.5518
G01 X86.2481 Y-0.5631
G01 X86.1878 Y-0.6750
G01 X86.1814 Y-0.6857
G01 X86.1104 Y-0.7912
G01 X86.1029 Y-0.8012
G01 X86.0220 Y-0.8993
G01 X86.0136 Y-0.9085
G01 X85.9235 Y-0.9982
G01 X85.9142 Y-1.0065
G01 X85.8158 Y-1.0870
G01 X85.8058 Y-1.0944
G01 X85.6999 Y-1.1648
G01 X85.6892 Y-1.1712
G01 X85.5770 Y-1.2310
G01 X85.5657 Y-1.2363
G01 X85.4481 Y-1.2848
G01 X85.4364 Y-1.2890
G01 X85.3147 Y-1.3258
G01 X85.3026 Y-1.3288
G01 X85.1779 Y-1.3535
G01 X85.1656 Y-1.3554
G01 X85.0390 Y-1.3678
G01 X85.0266 Y-1.3684
G01 X84.9630 Y-1.3700
G01 X45.8450 Y-1.3700
G00 Z2.0000
M05
G00 Z2.0000
G00 Z15.00


