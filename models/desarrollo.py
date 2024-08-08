# TODO 01:
#  Refactorizar
import datetime

def convert_hours(self, value):
    val = ''
    try:
        val = float(value)
    except Exception as e:
        print("Debe ingresar un número")
        exit()
    if val > 24.0:
        print("Debe ingresar un número menor a 24")
        exit()
    date = datetime.datetime.today().replace(hour=0, minute=0) + datetime.timedelta(hours=val)
    time = datetime.datetime.strftime(date,"%H:%M")
    return time

# TODO 02:
#  Refactorizar
@api.onchange('line_id')
def _get_packet_publishable_product_type(self):
    for record in self:
        product = record.product_id
        if product.publishable_ok:
            record.publishable_product_type = product.publishable_product_type
        else:
            record.publishable_product_type = 'notp'

# TODO 03:
#  Refactorizar
#  Agregar una condición para cualquier otro valor de 'publishable_product_type' lanzar una excepción de Odoo
#  Sustentar el tipo de excepción que usó(¿Por que?)
from odoo.exceptions import ValidationError
# Uso este tipo de excepción ya que dispara un mensaje para el usuario

def packet_product_action_publish(self):
    for rec in self:
        is_lan = False
        parameter_ids = self.env['guru.rule.country'].search([('code', '=', 'LAN')])
        if self.env.company.country_id.id in parameter_ids.country_ids.ids:
            is_lan = True
        product_id = rec.guru_product_id
        if product_id.publishable_ok:
            if product_id.product_tmpl_id.publishable_product_type == "pacom":
                res_model = 'guru.pacom.wzd'
                wzd_id = self.env[res_model].create({'var_obj': 'Obj', 'is_lan': is_lan})
                name = 'Pacom'
                view_id = [self.env.ref('guru_pacom.view_guru_pacom_simple_wzd_form').id]
            if product_id.product_tmpl_id.publishable_product_type == "landing_pacom":
                res_model = 'guru.landing.pacom.wzd'
                wzd_id = self.env[res_model].create({'var_obj': 'Obj'})
                name = 'Landing Pacom'
                view_id = [self.env.ref('guru_pacom.guru_landing_pacom_wzd_form_view').id]
            if product_id.product_tmpl_id.publishable_product_type == "web_shop":
                res_model = 'guru.web.product.wzd'
                wzd_id = self.env[res_model].create({'var_obj': 'Obj', 'is_lan': is_lan})
                line_id = rec.order_line_id.product_id.guru_packet_ids.filtered(
                    lambda e: e.publishable_product_type == 'web_shop')
                wzd_id.write({'plan_id': line_id.guru_product_id.plan_duda_id.id})
                name = 'Webs Shop'
                view_id = [self.env.ref('guru_pacom.guru_web_wzd_form_view').id]
            if product_id.product_tmpl_id.publishable_product_type == "web_vertical":
                res_model = 'guru.web.vertical.wzd'
                wzd_id = self.env[res_model].create({'var_obj': 'Obj', 'is_lan': is_lan})
                name = 'Tiendas WIX'
                view_id = [self.env.ref('guru_pacom.guru_web_vertical_wzd_form_view').id]
            if product_id.product_tmpl_id.publishable_product_type == "not_available":
                raise ValidationError("Atención. Producto no disponible")

            return {
                'name': _(name),
                'view_mode': 'form',
                'view_type': 'form',
                'view_id': view_id,
                'res_model': res_model,
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
        
# TODO 04:
#  Refactorizar
def get_select_sequence(self):
    select_list_sequence = []
    for i in range(10):
        select_list_sequence.append((str(i), str(i)))
    return select_list_sequence

# TODO 05:
#  Refactorizar
class SaleSubscriptionStage(models.Model):
    _inherit = 'sale.subscription.stage'

    category = fields.Selection(selection_add=[
        ('pause', 'Pause'), ('payu_process', 'PayU.PROCESS'), ('payment_error', 'Procesando')],
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
                    # mas arriba se filtro por code == 'GT' y move_type == 'out_refund', por lo tanto nunca entrará aqui
                    move.update({'edi_state': 'to_send'})
    self.env.cr.commit()

# TODO 07:
#  Refactorizar
#  En lugar de ambas funciones ¿Qué funciones usaría?
def check_user_in_group(self):
    user = self.env.user
    # 'Ajustes', 'Tipo de Pedido' Lista de nombres de los dos grupos
    # suponiendo que los XML ID sean base.group_system y sales_team.group_sale_manager
    if user.has_group('base.group_system') or user.has_group('sales_team.group_sale_manager'):
        return True
    return False

def check_user_in_group_config(self):
    user = self.env.user
    if user.has_group('base.group_system'):
        return True
    return False