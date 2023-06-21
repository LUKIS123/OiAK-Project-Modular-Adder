`timescale 1ns / 1ps

module hashedCell (
	input a,
	input b,
	input k,
	output h,
	output g,
	output p,
	output ap,
	output bp
	);
	
	assign g = a & b;
	assign p = a | b;
	assign h =  ~g & p;
	assign ap = k? ~h:h;
	assign bp = k? p:g;

endmodule

module envelopeCell (
	input ap,
	input bp,
	output hp,
	output pp,
	output gp
	);

	assign pp = ap | bp;
	assign gp = ap & bp;
	assign hp = !gp & pp;

endmodule
	
module blackNode (
	input p,
	input p1,
	input g,
	input g1,
	input pp,
	input pp1,
	input gp,
	input gp1,
	output op,
	output og,
	output opp,
	output ogp
	);

	assign op = p & p1;
	assign opp = pp & pp1;
	assign og = (p & g1) | g;
	assign ogp = (pp & gp1) | gp;

endmodule


module resultDecide (
    input h,
    input hp,
    input g,
    input gp,
    input c,
    output s
    );
    
    assign s = (c? hp:h) ^ (c? gp:g);
endmodule

module hashedCellBlock(
	input [n-1:0] a_v,
	input [n-1:0] b_v,
	input [n-1:0] k_v,
	output [n-1:0] h_v,
	output [n-1:0] g_v,
	output [n-1:0] p_v,
	output [n-1:0] ap_v,
	output [n:0] bp_v
	);
	
	parameter n =7;
	
	genvar i;
	generate
	    assign bp_v[0] = 0;
		for(i=0; i<n; i=i+1) begin: h_cell_gen
			hashedCell hcell_i(
				.a(a_v[i]),
				.b(b_v[i]),
				.k(k_v[i]),
				.h(h_v[i]),
				.g(g_v[i]),
				.p(p_v[i]),
				.ap(ap_v[i]),
				.bp(bp_v[i+1])
			);
		end
	endgenerate
endmodule

module EnvelopedCellBlock(
	input [n-1:0] ap_v,
	input [n:0] bp_v,
	output [n-1:0] gp_v,
	output [n-1:0] hp_v,
	output [n-1:0] pp_v
	);

	parameter n = 7;

	genvar i;
	generate
		for(i=0; i<n; i=i+1) begin: envbelopeCell_gen
              envelopeCell ecell_i(
                  	.ap(ap_v[i]),
                	.bp(bp_v[i]),
                  	.hp(hp_v[i]),
                  	.pp(pp_v[i]),
                  	.gp(gp_v[i])
              );
		end
	endgenerate
endmodule

module pararelPrefixStage(
	input [n-1:0] p_v,
	input [n-1:0] g_v,
	input [n-1:0] pp_v,
	input [n-1:0] gp_v,
	output [n-1:0] op_v,
	output [n-1:0] og_v,
	output [n-1:0] opp_v,
	output [n-1:0] ogp_v
	);

	wire [l:0][n-1:0] p;
	wire [l:0][n-1:0] g;
	wire [l:0][n-1:0] pp;
	wire [l:0][n-1:0] gp;
	
parameter n = 7;
parameter l = $clog2(n)-1;


	assign	p[0] = p_v;
	assign	g[0] = g_v;
	assign	pp[0] = pp_v;
	assign	gp[0] = gp_v;

	genvar i;
	generate
		for(i=0; i<l; i=i+1) begin
		genvar k;
			for(k=0;k<n; k=k+2*(2**i)) begin
			    genvar m;
			    for (m=0; m<2**i;m=m+1) begin
			        if(k+m <n) begin
			        	assign	p[i+1][k+m] = p[i][k+m];
	                    assign	g[i+1][k+m] = g[i][k+m];
	                    assign	pp[i+1][k+m] = pp[i][k+m];
	                    assign	gp[i+1][k+m] = gp[i][k+m];
	                    end
			        end
			
				genvar j;
				for(j=2**i; j<2*(2**i);j=j+1) begin
				if(k+j <n)
				    begin: blackNode_gen
					blackNode blackNode_i(
						.p(p[i][k+j]),
						.p1(p[i][k+2**i-1]),
						.g(g[i][k+j]),
						.g1(g[i][k+2**i-1]),
						.pp(pp[i][k+j]),
						.pp1(pp[i][k+2**i-1]),
						.gp(gp[i][k+j]),
						.gp1(gp[i][k+2**i-1]),
						.op(p[i+1][k+j]),
						.og(g[i+1][k+j]),
						.opp(pp[i+1][k+j]),
						.ogp(gp[i+1][k+j])
					);
				    end
				end
			end
		end
	endgenerate

	assign	op_v = p[l];
	assign	og_v = g[l];
	assign	opp_v = pp[l];
	assign	ogp_v = gp[l];
endmodule

module generateResult(
    input [n-1:0] h_v,
    input [n-1:0] hp_v,
    input [n-1:0] g_v,
    input [n-1:0] gp_v,
    input [n:0] bp_v,
    output [n-1:0] s_v
    );
    parameter n = 7;
    wire cout;
    
    assign cout = bp_v[n]? g_v[n-1]:gp_v[n-1];
    
    assign s_v[0] = cout ? hp_v[0]:h_v[0];
    
    genvar i;
    for(i=1;i<n;i=i+1) begin: resultDecide_gen
        resultDecide resultDecide_i(
        .h(h_v[i]),
        .hp(hp_v[i]),
        .g(g_v[i-1]),
        .gp(gp_v[i-1]),
        .c(cout),
        .s(s_v[i])
        );
    end
    
endmodule

module main;
 parameter N_bits = 7;
    assign stages = $clog2(N_bits);
    wire [N_bits-1:0] A_vector = 7'd21;
    wire [N_bits-1:0] B_vector = 7'd37;
    wire [N_bits-1:0] K_vector = 7'd59;
    
    wire [N_bits-1:0] S_vector;
    
    wire [N_bits-1:0] gi;
    wire [N_bits-1:0] hi;
    wire [N_bits-1:0] pi;
    wire [N_bits-1:0] api;
    wire [N_bits:0] bpi1;

	wire [N_bits-1:0] gi_prim;
	wire [N_bits-1:0] hi_prim;
	wire [N_bits-1:0] pi_prim;
	
	wire [N_bits-1:0] op;
	wire [N_bits-1:0] og;
	wire [N_bits-1:0] opp;
	wire [N_bits-1:0] ogp;

	 
	hashedCellBlock #(.n(N_bits)) hr(
	.a_v(A_vector), .b_v(B_vector), .k_v(K_vector),
	.h_v(hi), .g_v(gi), .p_v(pi), .ap_v(api), .bp_v(bpi1)
	);

	EnvelopedCellBlock #(.n(N_bits)) er(
	.ap_v(api), .bp_v(bpi1),
	.gp_v(gi_prim), .hp_v(hi_prim), .pp_v(pi_prim)
	);

	pararelPrefixStage #(.n(N_bits)) pr(
	.p_v(pi), .g_v(gi), .pp_v(pi_prim), .gp_v(gi_prim), 
	.op_v(op), .og_v(og), .opp_v(opp), .ogp_v(ogp)
	);

    generateResult #(.n(N_bits)) kr(
    .h_v(hi), .hp_v(hi_prim), .g_v(og), .gp_v(ogp), .bp_v(bpi1), .s_v(S_vector)
    );
    
    initial begin
        #1 $display("a = %b", A_vector);
        #1 $display("b = %b", B_vector);
        #1 $display("k = %b", K_vector);
		#1 $display("==========================================");
        //#1 $display("g = %b", gi);
		//#1 $display("h = %b", hi);
		//#1 $display("p = %b", pi);
		//#1 $display("a' = %b", api);
		//#1 $display("b' = %b", bpi1);
		//#1 $display("==========================================");
		//#1 $display("g' = %b", gi_prim);
		//#1 $display("h' = %b", hi_prim);
		//#1 $display("p' = %b", pi_prim);
		//#1 $display("==========================================");
		//#1 $display("op = %b", op);
		//#1 $display("og = %b", og);
		//#1 $display("op' = %b", opp);
		//#1 $display("og' = %b", ogp);
		//#1 $display("h   = %b", hi);
		//#1 $display("h'  = %b", hi_prim);
		//#1 $display("==========================================");
		//#1 $display("og  = %b", og);
		//#1 $display("og' = %b", ogp);
		//#1 $display("==========================================");
		#1 $display("s = %b", S_vector);

    end
endmodule
