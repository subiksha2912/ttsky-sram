`default_nettype none

module tt_um_memory (
    input  wire [7:0] ui_in,    
    output wire [7:0] uo_out,   
    input  wire [7:0] uio_in,   
    output wire [7:0] uio_out,  
    output wire [7:0] uio_oe,   
    input  wire       ena,      
    input  wire       clk,      
    input  wire       rst_n     
);

    // ----------------------------
    // Simple 4x8 Memory Mapping
    // ----------------------------

    wire rst = ~rst_n;

    wire        valid = ui_in[0];
    wire        wr_rd = ui_in[1];   // 1 = write, 0 = read
    wire [1:0]  addr  = ui_in[3:2];
    wire [7:0]  wdata = uio_in;

    wire        ready;
    wire [7:0]  rdata;

    // Instantiate memory (reduced size for TT)
    memory #(
        .DEPTH(4),
        .WIDTH(8)
    ) mem_inst (
        .clk(clk),
        .rst(rst),
        .valid(valid),
        .wr_rd(wr_rd),
        .addr(addr),
        .wdata(wdata),
        .ready(ready),
        .rdata(rdata)
    );

    // Outputs
    assign uo_out[0] = ready;
    assign uo_out[7:1] = rdata[6:0];

    assign uio_out = rdata;
    assign uio_oe  = (wr_rd == 0) ? 8'hFF : 8'h00;  // enable output during read

    // Prevent unused warnings
    wire _unused = &{ena, 1'b0};

endmodule


// ----------------------------
// MEMORY MODULE (unchanged core)
// ----------------------------
module memory #(
    parameter DEPTH = 4,
    parameter WIDTH = 8,
    parameter ADDR_WIDTH = $clog2(DEPTH)
)(
    input  wire                  clk,
    input  wire                  rst,
    input  wire                  valid,
    input  wire                  wr_rd,
    input  wire [ADDR_WIDTH-1:0] addr,
    input  wire [WIDTH-1:0]      wdata,

    output reg                   ready,
    output reg  [WIDTH-1:0]      rdata
);

    reg [WIDTH-1:0] mem [0:DEPTH-1];

    reg valid_d;
    reg wr_rd_d;
    reg [ADDR_WIDTH-1:0] addr_d;

    integer i;

    always @(posedge clk) begin
        if (rst) begin
            ready   <= 0;
            rdata   <= 0;
            valid_d <= 0;

            for (i = 0; i < DEPTH; i = i + 1)
                mem[i] <= 0;
        end 
        else begin
            valid_d <= valid;
            wr_rd_d <= wr_rd;
            addr_d  <= addr;

            ready <= 0;

            if (valid && wr_rd) begin
                mem[addr] <= wdata;
                ready <= 1;
            end

            if (valid_d && !wr_rd_d) begin
                rdata <= mem[addr_d];
                ready <= 1;
            end
        end
    end

endmodule
