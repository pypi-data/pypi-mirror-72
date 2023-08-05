import { Label, LabelView } from "@bokehjs/models/annotations/label";
import * as katex from "katex";
//"https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.0/katex.min.js"
//"https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.10.0/katex.min.css"
export class LatexLabelView extends LabelView {
    render() {
        // Here because AngleSpec does units tranform and label doesn't support specs
        let angle;
        switch (this.model.angle_units) {
            case "rad": {
                angle = -1 * this.model.angle;
                break;
            }
            case "deg": {
                angle = -1 * this.model.angle * Math.PI / 180.0;
                break;
            }
            default:
                throw new Error("unreachable");
        }
        const panel = this.panel || this.plot_view.frame;
        const xscale = this.plot_view.frame.xscales[this.model.x_range_name];
        const yscale = this.plot_view.frame.yscales[this.model.y_range_name];
        const { x, y } = this.model;
        let sx = this.model.x_units == "data" ? xscale.compute(x) : panel.xview.compute(x);
        let sy = this.model.y_units == "data" ? yscale.compute(y) : panel.yview.compute(y);
        sx += this.model.x_offset;
        sy -= this.model.y_offset;
        this._css_text(this.layer.ctx, "", sx, sy, angle);
        katex.render(this.model.text, this.el, { displayMode: true });
    }
}
LatexLabelView.__name__ = "LatexLabelView";
export class LatexLabel extends Label {
    static init_LatexLabel() {
        this.prototype.default_view = LatexLabelView;
    }
}
LatexLabel.__name__ = "LatexLabel";
LatexLabel.__module__ = "latex_label";
LatexLabel.init_LatexLabel();
//# sourceMappingURL=latex_label.js.map