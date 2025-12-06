<template>
    <div class="min-h-screen bg-background text-foreground p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold mb-2">Yeast Inventory</h1>
                <p class="text-muted-foreground">Manage your yeast strains and cultures</p>
            </div>
            <Button class="bg-primary hover:bg-primary/90" @click="showAddDialog = true">
                <Plus class="mr-2 h-4 w-4" />
                Add Yeast
            </Button>
        </div>

        <!-- Search and Filter -->
        <div class="flex gap-4 mb-6">
            <div class="flex-1">
                <Input
v-model="searchQuery" placeholder="Search yeasts by name, laboratory, type..."
                    class="bg-card border-input" />
            </div>
            <Select v-model="filterType">
                <SelectTrigger class="w-[180px] bg-card border-input">
                    <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="ale">Ale</SelectItem>
                    <SelectItem value="lager">Lager</SelectItem>
                    <SelectItem value="wild">Wild</SelectItem>
                </SelectContent>
            </Select>
        </div>

        <!-- Loading State -->
        <div v-if="yeastsLoading" class="flex justify-center items-center py-12">
            <div class="text-muted-foreground">Loading yeasts inventory...</div>
        </div>

        <!-- Error State -->
        <div
v-else-if="yeastsError"
            class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded">
            <p class="font-bold">Error loading yeasts</p>
            <p>{{ yeastsError }}</p>
        </div>

        <!-- Empty State -->
        <div
v-else-if="filteredYeasts.length === 0 && !searchQuery"
            class="text-center py-12 bg-card rounded-lg border border-border">
            <Package class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 class="text-lg font-semibold mb-2">No yeasts in inventory</h3>
            <p class="text-muted-foreground mb-4">Start by adding your first yeast strain</p>
            <Button class="bg-primary hover:bg-primary/90" @click="showAddDialog = true">
                <Plus class="mr-2 h-4 w-4" />
                Add First Yeast
            </Button>
        </div>

        <!-- Yeasts Table -->
        <div v-else class="bg-card rounded-lg border border-border overflow-hidden">
            <Table>
                <TableHeader>
                    <TableRow class="hover:bg-transparent border-border">
                        <TableHead>Name</TableHead>
                        <TableHead>Laboratory</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Form</TableHead>
                        <TableHead>Temp Range</TableHead>
                        <TableHead>Attenuation</TableHead>
                        <TableHead>Flocculation</TableHead>
                        <TableHead>Amount</TableHead>
                        <TableHead>Cost/Unit</TableHead>
                        <TableHead>Expiry</TableHead>
                        <TableHead class="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow
v-for="yeast in filteredYeasts" :key="yeast.id" class="border-border hover:bg-accent/50"
                        :class="{ 'bg-destructive/10': isLowStock(yeast.amount) || isExpiringSoon(yeast.expiry_date) }">
                        <TableCell class="font-medium">
                            <div>{{ yeast.name }}</div>
                            <div v-if="yeast.product_id" class="text-xs text-muted-foreground">{{ yeast.product_id }}
                            </div>
                        </TableCell>
                        <TableCell>{{ yeast.laboratory || 'N/A' }}</TableCell>
                        <TableCell>
                            <Badge variant="outline">{{ yeast.type }}</Badge>
                        </TableCell>
                        <TableCell>
                            <Badge :variant="yeast.form === 'liquid' ? 'default' : 'secondary'">
                                {{ yeast.form }}
                            </Badge>
                        </TableCell>
                        <TableCell>
                            <span v-if="yeast.min_temperature && yeast.max_temperature">
                                {{ yeast.min_temperature }}°C - {{ yeast.max_temperature }}°C
                            </span>
                            <span v-else class="text-muted-foreground">N/A</span>
                        </TableCell>
                        <TableCell>{{ yeast.attenuation ? `${yeast.attenuation}%` : 'N/A' }}</TableCell>
                        <TableCell>
                            <Badge v-if="yeast.flocculation" variant="outline">
                                {{ yeast.flocculation }}
                            </Badge>
                            <span v-else class="text-muted-foreground">N/A</span>
                        </TableCell>
                        <TableCell>
                            <span :class="{ 'text-destructive font-bold': isLowStock(yeast.amount) }">
                                {{ yeast.amount }} {{ yeast.unit }}
                            </span>
                        </TableCell>
                        <TableCell>
                            {{ yeast.cost_per_unit ? `€${yeast.cost_per_unit.toFixed(2)}` : 'N/A' }}
                        </TableCell>
                        <TableCell>
                            <span :class="{ 'text-destructive font-bold': isExpiringSoon(yeast.expiry_date) }">
                                {{ yeast.expiry_date ? formatDate(yeast.expiry_date) : 'N/A' }}
                            </span>
                        </TableCell>
                        <TableCell class="text-right">
                            <div class="flex justify-end gap-2">
                                <Button variant="ghost" size="sm" @click="editYeast(yeast)">
                                    <Edit class="h-4 w-4" />
                                </Button>
                                <Button
variant="ghost" size="sm" class="text-destructive hover:text-destructive hover:bg-destructive/10"
                                    @click="confirmDelete(yeast)">
                                    <Trash2 class="h-4 w-4" />
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>

        <!-- Summary Stats -->
        <div v-if="yeasts.length > 0" class="grid grid-cols-4 gap-4 mt-6">
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Strains</div>
                <div class="text-2xl font-bold">{{ yeasts.length }}</div>
            </div>
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Low Stock Items</div>
                <div class="text-2xl font-bold text-destructive">{{ lowStockCount }}</div>
            </div>
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Value</div>
                <div class="text-2xl font-bold">€{{ totalValue.toFixed(2) }}</div>
            </div>
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Expiring Soon</div>
                <div class="text-2xl font-bold text-destructive">{{ expiringSoonCount }}</div>
            </div>
        </div>

        <!-- Add/Edit Dialog -->
        <Dialog v-model:open="showAddDialog">
            <DialogContent class="bg-card border-border max-w-3xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>{{ editingYeast ? 'Edit Yeast' : 'Add New Yeast' }}</DialogTitle>
                </DialogHeader>
                <div class="grid grid-cols-2 gap-4 py-4">
                    <div class="col-span-2">
                        <Label for="name">Name *</Label>
                        <Input
id="name" v-model="formData.name" placeholder="e.g., SafAle US-05"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="laboratory">Laboratory</Label>
                        <Input
id="laboratory" v-model="formData.laboratory" placeholder="e.g., Fermentis"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="product_id">Product ID</Label>
                        <Input
id="product_id" v-model="formData.product_id" placeholder="e.g., US-05"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="type">Type *</Label>
                        <Select v-model="formData.type">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="ale">Ale</SelectItem>
                                <SelectItem value="lager">Lager</SelectItem>
                                <SelectItem value="wild">Wild</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="form">Form *</Label>
                        <Select v-model="formData.form">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select form" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="dry">Dry</SelectItem>
                                <SelectItem value="liquid">Liquid</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="min_temperature">Min Temperature (°C)</Label>
                        <Input
id="min_temperature" v-model.number="formData.min_temperature" type="number" step="0.5"
                            placeholder="e.g., 15" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="max_temperature">Max Temperature (°C)</Label>
                        <Input
id="max_temperature" v-model.number="formData.max_temperature" type="number" step="0.5"
                            placeholder="e.g., 24" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="attenuation">Attenuation (%)</Label>
                        <Input
id="attenuation" v-model.number="formData.attenuation" type="number" step="1"
                            placeholder="e.g., 75" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="flocculation">Flocculation</Label>
                        <Select v-model="formData.flocculation">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select flocculation" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="low">Low</SelectItem>
                                <SelectItem value="medium">Medium</SelectItem>
                                <SelectItem value="high">High</SelectItem>
                                <SelectItem value="very high">Very High</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="amount">Amount *</Label>
                        <Input
id="amount" v-model.number="formData.amount" type="number" step="1" placeholder="e.g., 5"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="unit">Unit *</Label>
                        <Select v-model="formData.unit">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select unit" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="packets">Packets</SelectItem>
                                <SelectItem value="vials">Vials</SelectItem>
                                <SelectItem value="g">Grams (g)</SelectItem>
                                <SelectItem value="ml">Milliliters (ml)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="supplier">Supplier</Label>
                        <Input
id="supplier" v-model="formData.supplier" placeholder="e.g., BrewStore"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="cost_per_unit">Cost per Unit (€)</Label>
                        <Input
id="cost_per_unit" v-model.number="formData.cost_per_unit" type="number" step="0.01"
                            placeholder="e.g., 4.50" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="manufacture_date">Manufacture Date</Label>
                        <Input
id="manufacture_date" v-model="formData.manufacture_date" type="date"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="expiry_date">Expiry Date</Label>
                        <Input
id="expiry_date" v-model="formData.expiry_date" type="date"
                            class="bg-background border-input" />
                    </div>

                    <div class="col-span-2">
                        <Label for="notes">Notes</Label>
                        <Textarea
id="notes" v-model="formData.notes" placeholder="Additional notes..."
                            class="bg-background border-input" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Cancel</Button>
                    <Button :disabled="!isFormValid" class="bg-primary hover:bg-primary/90" @click="saveYeast">
                        {{ editingYeast ? 'Update' : 'Add' }} Yeast
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Plus, Edit, Trash2, Package } from 'lucide-vue-next'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Textarea } from '~/components/ui/textarea'
import { Badge } from '~/components/ui/badge'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '~/components/ui/table'
import {
    Dialog,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '~/components/ui/dialog'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '~/components/ui/select'
import type { InventoryYeast } from '~/composables/useInventory'

const {
    yeasts,
    yeastsLoading,
    yeastsError,
    fetchYeasts,
    addYeast,
    updateYeast,
    removeYeast
} = useInventory()

// Search and filter
const searchQuery = ref('')
const filterType = ref('all')

// Dialog state
const showAddDialog = ref(false)
const editingYeast = ref<InventoryYeast | null>(null)

// Form data
const formData = ref({
    name: '',
    laboratory: '',
    product_id: '',
    type: 'ale',
    form: 'dry',
    min_temperature: 0,
    max_temperature: 0,
    attenuation: 0,
    flocculation: '',
    amount: 0,
    unit: 'packets',
    supplier: '',
    cost_per_unit: 0,
    manufacture_date: '',
    expiry_date: '',
    notes: '',
})

// Computed
const filteredYeasts = computed(() => {
    let filtered = yeasts.value

    // Filter by type
    if (filterType.value !== 'all') {
        filtered = filtered.filter(y => y.type === filterType.value)
    }

    // Filter by search
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(y =>
            y.name.toLowerCase().includes(query) ||
            y.laboratory?.toLowerCase().includes(query) ||
            y.product_id?.toLowerCase().includes(query) ||
            y.type?.toLowerCase().includes(query) ||
            y.supplier?.toLowerCase().includes(query)
        )
    }

    return filtered
})

const lowStockCount = computed(() => {
    return yeasts.value.filter(y => isLowStock(y.amount)).length
})

const expiringSoonCount = computed(() => {
    return yeasts.value.filter(y => isExpiringSoon(y.expiry_date)).length
})

const totalValue = computed(() => {
    return yeasts.value.reduce((total, y) => {
        return total + (y.cost_per_unit || 0) * y.amount
    }, 0)
})

const isFormValid = computed(() => {
    return formData.value.name &&
        formData.value.type &&
        formData.value.form &&
        formData.value.amount > 0 &&
        formData.value.unit
})

// Methods
function isLowStock(amount: number): boolean {
    return amount < 2 // Less than 2 packets/vials
}

function isExpiringSoon(expiryDate?: string): boolean {
    if (!expiryDate) return false
    const expiry = new Date(expiryDate)
    const today = new Date()
    const diffDays = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
    return diffDays >= 0 && diffDays < 60 // Expiring within 60 days
}

function formatDate(dateString: string): string {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    })
}

function editYeast(yeast: InventoryYeast) {
    editingYeast.value = yeast
    formData.value = {
        name: yeast.name,
        laboratory: yeast.laboratory || '',
        product_id: yeast.product_id || '',
        type: yeast.type,
        form: yeast.form,
        min_temperature: yeast.min_temperature || 0,
        max_temperature: yeast.max_temperature || 0,
        attenuation: yeast.attenuation || 0,
        flocculation: yeast.flocculation || '',
        amount: yeast.amount,
        unit: yeast.unit,
        supplier: yeast.supplier || '',
        cost_per_unit: yeast.cost_per_unit || 0,
        manufacture_date: yeast.manufacture_date || '',
        expiry_date: yeast.expiry_date || '',
        notes: yeast.notes || '',
    }
    showAddDialog.value = true
}

async function saveYeast() {
    if (!isFormValid.value) return

    if (editingYeast.value) {
        await updateYeast(editingYeast.value.id, formData.value)
    } else {
        await addYeast(formData.value)
    }

    cancelEdit()
}

function cancelEdit() {
    showAddDialog.value = false
    editingYeast.value = null
    formData.value = {
        name: '',
        laboratory: '',
        product_id: '',
        type: 'ale',
        form: 'dry',
        min_temperature: 0,
        max_temperature: 0,
        attenuation: 0,
        flocculation: '',
        amount: 0,
        unit: 'packets',
        supplier: '',
        cost_per_unit: 0,
        manufacture_date: '',
        expiry_date: '',
        notes: '',
    }
}

async function confirmDelete(yeast: InventoryYeast) {
    if (confirm(`Are you sure you want to delete ${yeast.name}?`)) {
        await removeYeast(yeast.id)
    }
}

// Lifecycle
onMounted(async () => {
    await fetchYeasts()
})
</script>
