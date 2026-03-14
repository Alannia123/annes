/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FeeOverview extends Component {

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.action = useService("action");

        this.state = useState({
            search: "",
            roll_no: null,
            division_id: null,
            academic_years: [],
            fees: [],
            divisions: [],
            selected_fee_ids: [],
            loading: false,

            // ✅ Payment fields
            payment_date: new Date().toISOString().split("T")[0],
            payment_mode: "cash",
        });

        onWillStart(async () => {
            await this.loadDivisions();
            await this.loadFees();
        });
    }


    openStudentFees(ev) {

    const record_id = parseInt(ev.currentTarget.dataset.id);

    console.log("Clicked record:", record_id);

    if (!record_id) {
        return;
    }

    this.action.doAction({
        type: "ir.actions.act_window",
        res_model: "student.fees",
        res_id: record_id,
        views: [[false, "form"]],
        target: "current",
    });
}

    async loadDivisions() {
        this.state.divisions = await this.orm.searchRead(
            "education.class.division",
            [],
            ["name"]
        );
    }

    async loadFees() {
        this.state.loading = true;

        this.state.fees = await this.orm.call(
            "student.fee.line",
            "get_fee_lines",
            [],
            {
                search: this.state.search,
                roll_no: this.state.roll_no,
                division_id: this.state.division_id,
            }
        );

        this.state.loading = false;
    }

    async onSearch(ev) {
        this.state.search = ev.target.value;
        await this.loadFees();
    }

    async onDivisionChange(ev) {
        this.state.division_id = ev.target.value
            ? parseInt(ev.target.value)
            : null;
        await this.loadFees();
    }

    async onRollSearch(ev) {

        const value = ev.target.value.trim();

        if (!value) {
            this.state.roll_no = null;
            await this.loadFees();
            return;
        }

        if (!this.state.division_id) {
            this.notification.add(
                "Please select division before searching by Roll No.",
                { type: "warning" }
            );
            ev.target.value = "";
            return;
        }

        this.state.roll_no = parseInt(value);
        await this.loadFees();
    }

    toggleFee(ev) {
        const feeId = parseInt(ev.target.dataset.id);

        if (ev.target.checked) {
            this.state.selected_fee_ids.push(feeId);
        } else {
            this.state.selected_fee_ids =
                this.state.selected_fee_ids.filter(id => id !== feeId);
        }
    }
//Get Selected total
    getSelectedTotal(student) {
        let total = 0;

        for (const fee of student.fees) {
            if (this.state.selected_fee_ids.includes(fee.id)) {
                total += fee.amount;
            }
        }

        return total;
    }
    //Get Selected Fine total
    getSelectedFine(student) {
        let total = 0;

        for (const fee of student.fees) {
            if (this.state.selected_fee_ids.includes(fee.id)) {
                total += fee.fine_amount;
            }
        }

        return total;
    }//Get Selected total
    getSelectedConTotal(student) {
        let total = 0;

        for (const fee of student.fees) {
            if (this.state.selected_fee_ids.includes(fee.id)) {
                total += fee.concession_amount;
            }
        }

        return total;
    }

viewStudentBill(ev) {

    const feeId = parseInt(ev.currentTarget.dataset.fee);

    if (!feeId) {
        this.notification.add("No bill found.", { type: "warning" });
        return;
    }

    const url = `/report/pdf/mis_education_fee.report_mis_fee_invoices/${feeId}`;

    window.open(url, "_blank");
}

    async payStudentFees(ev) {

    const studentId = parseInt(ev.target.dataset.student);
    const student = this.state.fees.find(s => s.id === studentId);

    if (!student) {
        return;
    }

    const selectedFees = student.fees
        .filter(f => this.state.selected_fee_ids.includes(f.id))
        .map(f => f.id);

    if (!selectedFees.length) {
        this.notification.add("Please select at least one fee to pay.", {
            type: "warning",
        });
        return;
    }

    const result = await this.orm.call(
    "student.fee.line",
    "action_pay_selected_fees",
    [selectedFees],
    {
        payment_date: this.state.payment_date,
        payment_mode: this.state.payment_mode,
    }
);

console.log("RESULT:", result);

if (result && result.report_name) {
    const url = `/report/pdf/${result.report_name}/${result.res_id}`;
    window.open(url, "_blank");
}

    this.notification.add("Selected fees processed 6666successfully.", {
        type: "success",
    });

    this.state.selected_fee_ids = this.state.selected_fee_ids.filter(
        id => !selectedFees.includes(id)
    );

    await this.loadFees();
}
}

FeeOverview.template = "mis_education_fee.FeeOverview";
registry.category("actions").add("erp_fee_overview_tag", FeeOverview);