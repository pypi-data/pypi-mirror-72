import { Label, LabelView } from "@bokehjs/models/annotations/label";
export declare class LatexLabelView extends LabelView {
    model: LatexLabel;
    render(): void;
}
export declare class LatexLabel extends Label {
    static __module__: string;
    static init_LatexLabel(): void;
}
