# TODO 01:
#  Refactorizar
def convert_hours(self, value):
    val = ''
    if value == '1':
        val = '01:00'
    if value == '1.5':
        val = '01:30'
    if value == '2':
        val = '02:00'
    if value == '2.5':
        val = '02:30'
    if value == '3':
        val = '03:00'
    if value == '3.5':
        val = '03:30'
    if value == '4':
        val = '04:00'
    if value == '4.5':
        val = '04:30'
    if value == '5':
        val = '05:00'
    if value == '5.5':
        val = '05:30'
    if value == '6':
        val = '06:00'
    if value == '6.5':
        val = '06:30'
    if value == '7':
        val = '07:00'
    if value == '7.5':
        val = '07:30'
    if value == '8':
        val = '08:00'
    if value == '8.5':
        val = '08:30'
    if value == '9':
        val = '09:00'
    if value == '9.5':
        val = '09:30'
    if value == '10':
        val = '10:00'
    if value == '10.5':
        val = '10:30'
    if value == '11':
        val = '11:00'
    if value == '11.5':
        val = '11:30'
    if value == '12':
        val = '12:00'
    if value == '12.5':
        val = '12:30'
    if value == '13':
        val = '13:00'
    if value == '13.5':
        val = '13:30'
    if value == '14':
        val = '14:00'
    if value == '14.5':
        val = '15:30'
    if value == '15':
        val = '15:00'
    if value == '15.5':
        val = '15:30'
    if value == '16':
        val = '16:00'
    if value == '16.5':
        val = '16:30'
    if value == '17':
        val = '17:00'
    if value == '17.5':
        val = '17:30'
    if value == '18':
        val = '18:00'
    if value == '18.5':
        val = '18:30'
    if value == '19':
        val = '19:00'
    if value == '19.5':
        val = '19:30'
    if value == '20':
        val = '20:00'
    if value == '20.5':
        val = '20:30'
    if value == '21':
        val = '21:00'
    if value == '21.5':
        val = '21:30'
    if value == '22':
        val = '22:00'
    if value == '22.5':
        val = '22:30'
    if value == '23':
        val = '23:00'
    if value == '23.5':
        val = '23:30'
    if value == '23.9':
        val = '23:59'
    if value == '0':
        val = '00:00'
    if value == '0.5':
        val = '00:30'
    return val


# TODO 02:
#  Refactorizar
@api.onchange('line_id')
def _get_packet_publishable_product_type(self):
    if self:
        for record in self:
            data_products = record.env['product.product'].search([('id', '=', record.product_id.id)])
            for data_product in data_products:
                if data_product:
                    for data in data_product:
                        if data.publishable_ok:
                            record.publishable_product_type = data.publishable_product_type
                        else:
                            record.publishable_product_type = 'notp'
                else:
                    record.publishable_product_type = 'notp'


# TODO 03:
#  Refactorizar
#  Agregar una condición para cualquier otro valor de 'publishable_product_type' lanzar una excepción de Odoo
#  Sustentar el tipo de excepción que usó(¿Por que?)
def packet_product_action_publish(self):
    for rec in self:
        is_lan = False
        parameter_ids = self.env['guru.rule.country'].search([('code', '=', 'LAN')])
        if self.env.company.country_id.id in parameter_ids.country_ids.ids:
            is_lan = True
        data_product = self.env['product.product'].search([('id', '=', rec.guru_product_id.id)])
        is_product_packet = True
        for data in data_product:
            if data.publishable_ok:
                if data.product_tmpl_id.publishable_product_type == "pacom":
                    wzd_id = self.env['guru.pacom.wzd'].create({'var_obj': 'Obj', 'is_lan': is_lan})
                    return {
                        'name': _('Pacom'),
                        'view_mode': 'form',
                        'view_type': 'form',
                        'view_id': [self.env.ref('guru_pacom.view_guru_pacom_simple_wzd_form').id],
                        'res_model': 'guru.pacom.wzd',
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'res_id': wzd_id.id,
                        'context': {
                            'packet_product_line': rec.id,
                            'line_id': rec.order_line_id.id,
                            'order_id': rec.order_id.id,
                            'partner_id': rec.order_id.partner_id.id,
                        },
                    }
                if data.product_tmpl_id.publishable_product_type == "landing_pacom":
                    wzd_landing_id = self.env['guru.landing.pacom.wzd'].create({'var_obj': 'Obj'})
                    return {
                        'name': _('Landing Pacom'),
                        'view_mode': 'form',
                        'view_type': 'form',
                        'view_id': [self.env.ref('guru_pacom.guru_landing_pacom_wzd_form_view').id],
                        'res_model': 'guru.landing.pacom.wzd',
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'res_id': wzd_landing_id.id,
                        'context': {
                            'packet_product_line': rec.id,
                            'line_id': rec.order_line_id.id,
                            'order_id': rec.order_id.id,
                            'partner_id': rec.order_id.partner_id.id,
                        },
                    }
                if data.product_tmpl_id.publishable_product_type == "web_shop":
                    wzd_web_id = self.env['guru.web.product.wzd'].create({'var_obj': 'Obj', 'is_lan': is_lan})
                    line_id = rec.order_line_id.product_id.guru_packet_ids.filtered(
                        lambda e: e.publishable_product_type == 'web_shop')
                    wzd_web_id.write({'plan_id': line_id.guru_product_id.plan_duda_id.id})
                    return {
                        'name': _('Webs Shop'),
                        'view_mode': 'form',
                        'view_type': 'form',
                        'view_id': [self.env.ref('guru_pacom.guru_web_wzd_form_view').id],
                        'res_model': 'guru.web.product.wzd',
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'res_id': wzd_web_id.id,
                        'context': {
                            'packet_product_line': rec.id,
                            'line_id': rec.order_line_id.id,
                            'order_id': rec.order_id.id,
                            'partner_id': rec.order_id.partner_id.id,
                        },
                    }
                if data.product_tmpl_id.publishable_product_type == "web_vertical":
                    wzd_web_id = self.env['guru.web.vertical.wzd'].create({'var_obj': 'Obj', 'is_lan': is_lan})
                    line_id = rec.order_line_id.product_id.guru_packet_ids.filtered(
                        lambda e: e.publishable_product_type == 'web_vertical')
                    return {
                        'name': _('Tiendas WIX'),
                        'view_mode': 'form',
                        'view_type': 'form',
                        'view_id': [self.env.ref('guru_pacom.guru_web_vertical_wzd_form_view').id],
                        'res_model': 'guru.web.vertical.wzd',
                        'type': 'ir.actions.act_window',
                        'target': 'new',
                        'res_id': wzd_web_id.id,
                        'context': {
                            'packet_product_line': rec.id,
                            'line_id': rec.order_line_id.id,
                            'order_id': rec.order_id.id,
                            'partner_id': rec.order_id.partner_id.id,
                        },
                    }

# TODO 04:
#  Refactorizar
def get_select_sequence(self):
    select_list_sequence = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                            ('8', '8'), ('9', '9'), ('10', '10')]
    return select_list_sequence


# TODO 05:
#  Refactorizar
class SaleSubscriptionStage(models.Model):
    _inherit = 'sale.subscription.stage'

    category = fields.Selection(selection_add=[
        ('pause', 'Pause')],
        ondelete={'pause': 'set default'},
        required=True, default='draft', help="Category of the stage")


class SaleSubscriptionStage(models.Model):
    _inherit = 'sale.subscription.stage'

    category = fields.Selection(selection_add=[
        ('payu_process', 'PayU.PROCESS')],
        ondelete={'pause': 'set default'},
        required=True, default='draft', help="Category of the stage")


class SaleSubscriptionStage(models.Model):
    _inherit = 'sale.subscription.stage'

    category = fields.Selection(selection_add=[
        ('payment_error', 'Procesando')],
        ondelete={'pause': 'set default'},
        required=True, default='draft', help="Category of the stage")

# TODO 06:
#  Refactorizar
#  Indicar que se hizo mal en esta función.
def _post(self, soft=True):
    # ejecuta el comportamiento del post segun el flujo de la funcion nativa
    res = super(AccountMove, self)._post(soft)
    for move in res.filtered(
        lambda m: m.company_id.country_id.code == 'GT' and m.move_type == 'out_refund'
    ):
        if (move.reversed_entry_id
                and move.reversed_entry_id.l10n_gt_reverse_with_nabn
                and move.journal_id.code != 'NABN'):
            raise UserError('En la nota de abono debe utilizar el diario "Nota de Abono"')
        for line_id in move.line_ids:
            line_id.ctrl_cta_ctble_nabn()
            if move.company_id.country_id.code == 'PE' and move.move_type == 'out_invoice' and move.debit_note is False:
                if move.journal_id.edi_format_ids and move.state == 'draft':
                    move.update({'edi_state': 'to_send'})
    self.env.cr.commit()


# TODO 07:
#  Refactorizar
#  En lugar de ambas funciones ¿Qué funciones usaría?
def check_user_in_group(self):
    user = self.env.user
    flag = False
    group_names = ['Ajustes', 'Tipo de Pedido']  # Lista de nombres de los dos grupos
    groups = self.env['res.groups'].search([('name', 'in', group_names)])
    if user and groups:
        for group in groups:
            ls_users = group.users
            for name in ls_users:
                if name.name == user.name:
                    flag = True
    if flag:
        return True
    else:
        return False

def check_user_in_group_config(self):
    user = self.env.user
    flag = False
    groups = self.env['res.groups'].search([('name', '=', 'Ajustes')], limit=1)
    if user and groups:
        for group in groups:
            ls_users = group.users
            for name in ls_users:
                if name.name == user.name:
                    flag = True
    if flag:
        return True
    else:
        return False