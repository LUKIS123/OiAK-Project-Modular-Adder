module hashedCell (a, b, k, h, g, p, ap, bp);
	input wire a;
	input wire b;
	input wire k;
	output wire h;
	output wire g;
	output wire p;
	output wire ap;
	output wire bp;
	
	always @(*)
		begin
			g = a & b;
			p = a | b;
			h = p & !g;
          if (k) begin
            ap = !h; end
			else
              ap = h;
          if (k) begin
            bp = p; end
			else
				bp= g;
		end
endmodule

module envelopeCell (ap, bp, hp, pp, gp);
	input wire ap;
	input wire bp;
	output wire hp;
	output wire pp;
	output wire gp;

	always @(*)
		begin
			pp = ap | bp;
			gp = ap & bp;
			hp = !gp & pp;
		end
endmodule
	
module blackNode (p, p1, g, g1, pp, pp1, gp, gp1, op, og, opp, ogp);
	input wire p;
	input wire p1;
	input wire g;
	input wire g1;
	input wire pp;
	input wire pp1;
	input wire gp;
	input wire gp1;
	output wire op;
	output wire og;
	output wire opp;
	output wire ogp;
	
	always @(*)
		begin
			op = p & p1;
			opp = pp & pp1;
			og = (p & g1) | g;
			ogp = (pp & gp1) | gp;
		end
endmodule

module hashedCellBlock(a_v, b_v, k_v, h_v, g_v, p_v, ap_v, bp_v);
	input wire [n-1:0] a_v;
	input wire [n-1:0] b_v;
	input wire [n-1:0] k_v;
	output wire [n-1:0] h_v;
	output wire [n-1:0] g_v;
	output wire [n-1:0] p_v;
	output wire [n-1:0] ap_v;
	output wire [n-1:0] bp_v;
	
	parameter n =7;
	
	genvar i;
	
	generate
		for(i=0; i<WIDTH; i=i+1) begin: h_cell_gen
			HashedCell hcell_i(
				.a(a_v[i]),
				.b(a_v[i]),
				.k(k_v[i]),
				.g(g_v[i]),
				.h(h_v[i]),
				.p(p_v[i]),
				.ap(ap_v[i]),
				.bp(bp_v[i])
			);
		end
	endgenerate
endmodule

module EnvelopedCellBlock(ap_v, bp_v, gp_v, hp_v, pp_v);
	input wire [n-1:0] ap_v;
	input wire [n-1:0] bp_v;
	output wire [n-1:0] gp_v;
	output wire [n-1:0] hp_v;
	output wire[n-1:0] pp_v;

	parameter n = 7;

	genvar i;
	generate
		for(i=0; i<WIDTH; i=i+1) begin: envbelopeCell_gen
          if(i==0) begin
              EnvelopedCell ecell_i(
                  	.ap(ap_v[i]),
                	.bp(0),
                  	.hp(hp_v[i]),
                  	.pp(pp_v[i]),
                  	.gp(gp_v[i])
              );
            end 
            else begin
              EnvelopedCell ecell_i(
                  	.ap(ap_v[i]),
                	.bp(bp_v[i-1]),
                  	.hp(hp_v[i]),
                  	.pp(pp_v[i]),
                  	.gp(gp_v[i])
              );
            end
		end
	endgenerate
endmodule

module pararelPrefixStage(p_v, p1_v, g_v, g1_v, pp_v, pp1_v, gp_v, gp1_v, op_v, og_v, opp_v, ogp_v);
	input wire [n-1:0] p_v;
	input wire [n-1:0] p1_v;
	input wire [n-1:0] g_v;
	input wire [n-1:0] g1_v;
	input wire [n-1:0] pp_v;
	input wire [n-1:0] pp1v;
	input wire [n-1:0] gp_v;
	input wire [n-1:0] gp1_v;
	output wire [n-1:0] op_v;
	output wire [n-1:0] og_v;
	output wire [n-1:0] opp_v;
	output wire [n-1:0] ogpv;
	
	parameter n = 7;
	
	genvar i;
	generate
		for(i=0; i<WIDTH; i=i+1) begin: h_cell_gen
			HashedCell hcell_i(
				.a(a_v[i]),
				.b(a_v[i]),
				.k(k_v[i]),
				.g(g_v[i]),
				.h(h_v[i]),
				.p(p_v[i]),
				.ap(ap_v[i]),
				.bp(bp_v[i])
			);
		end
	endgenerate
	