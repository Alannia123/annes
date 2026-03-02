/** @odoo-module **/

import { Component, xml, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class AppsMenuPreferences extends Component {
    setup() {
        this.action = useService("action");
        this.user = useService("user");

        // reactive state
        this.state = useState({ isAdmin: false });

        // fire async check
        this.loadGroups();
    }

    async loadGroups() {
        try {
            this.state.isAdmin = await this.user.hasGroup("base.group_system");
        } catch (e) {
            console.error("Group check failed:", e);
        }
    }

    async _onClick() {
        const action = await this.action.loadAction(
            "web_responsive.res_users_view_form_apps_menu_preferences_action"
        );
        this.action.doAction({ ...action, res_id: this.user.userId });
    }
    async _onrefreshClick() {
        this.action.doAction({ type: "ir.actions.client", tag: "reload" });
    }
}

AppsMenuPreferences.template = xml`


    <div class="o-dropdown dropdown o-dropdown--no-caret">
        <button
            role="button"
            type="button"
            title="Refresh"
            class="dropdown-toggle o-dropdown--narrow"
            t-on-click="_onrefreshClick">
                <i class="fa fa-refresh fa-lg px-1"/>
        </button>
    </div>

    <div class="o-dropdown dropdown o-dropdown--no-caret" t-if="state.isAdmin">
        <button
            type="button"
            class="dropdown-toggle o-dropdown--narrow"
            title="App Menu Preferences"
            t-on-click="_onClick">
            <i class="fa fa-tint fa-lg px-1"/>
        </button>
    </div>
`;

registry.category("systray").add("AppMenuTheme", {
    Component: AppsMenuPreferences,
}, { sequence: 100 });
