import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Check, X } from 'lucide-react-native';
import { COLORS, SPACING } from '../constants/theme';
import GradientButton from '../components/GradientButton';

export default function SubscriptionScreen({ navigation }) {

    const handlePurchase = () => {
        // Determine payment logic here
        alert("This is a demo. In the real app, this opens Google Play Billing.");
        navigation.goBack();
    };

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView contentContainerStyle={styles.content}>
                <TouchableOpacity style={styles.closeButton} onPress={() => navigation.goBack()}>
                    <X color={COLORS.textSecondary} size={24} />
                </TouchableOpacity>

                <Text style={styles.title}>Unlock ATLAS AI</Text>
                <Text style={styles.subtitle}>Supercharge your studies with unlimited power.</Text>

                <View style={styles.pricingCard}>
                    <Text style={styles.tierName}>PREMIUM</Text>
                    <View style={styles.priceContainer}>
                        <Text style={styles.currency}>JOD</Text>
                        <Text style={styles.price}>1.00</Text>
                        <Text style={styles.period}>/month</Text>
                    </View>
                    <Text style={styles.cancelText}>Cancel anytime</Text>

                    <View style={styles.divider} />

                    <View style={styles.featureRow}>
                        <Check color={COLORS.success} size={20} />
                        <Text style={styles.featureText}>Unlimited Question Scans</Text>
                    </View>
                    <View style={styles.featureRow}>
                        <Check color={COLORS.success} size={20} />
                        <Text style={styles.featureText}>Unlimited PDF Uploads</Text>
                    </View>
                    <View style={styles.featureRow}>
                        <Check color={COLORS.success} size={20} />
                        <Text style={styles.featureText}>Detailed Explanations</Text>
                    </View>
                    <View style={styles.featureRow}>
                        <Check color={COLORS.success} size={20} />
                        <Text style={styles.featureText}>Priority AI Engine (Faster)</Text>
                    </View>
                    <View style={styles.featureRow}>
                        <Check color={COLORS.success} size={20} />
                        <Text style={styles.featureText}>No Ads</Text>
                    </View>
                </View>

                <GradientButton
                    title="Subscribe for 1 JOD"
                    onPress={handlePurchase}
                    style={styles.subscribeButton}
                />

                <Text style={styles.legalText}>
                    Payment will be charged to your Google Play account. Subscription automatically renews unless auto-renew is turned off at least 24-hours before the end of the current period.
                </Text>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: COLORS.background,
    },
    content: {
        padding: SPACING.l,
        alignItems: 'center',
    },
    closeButton: {
        alignSelf: 'flex-start',
        marginBottom: SPACING.l,
    },
    title: {
        color: COLORS.text,
        fontSize: 32,
        fontWeight: 'bold',
        marginBottom: SPACING.s,
        textAlign: 'center',
    },
    subtitle: {
        color: COLORS.textSecondary,
        fontSize: 16,
        marginBottom: SPACING.xl,
        textAlign: 'center',
    },
    pricingCard: {
        backgroundColor: COLORS.surface,
        width: '100%',
        borderRadius: 24,
        padding: SPACING.xl,
        borderWidth: 1,
        borderColor: COLORS.primary,
        marginBottom: SPACING.xl,
    },
    tierName: {
        color: COLORS.primary,
        fontWeight: 'bold',
        letterSpacing: 2,
        marginBottom: SPACING.m,
        textAlign: 'center',
    },
    priceContainer: {
        flexDirection: 'row',
        alignItems: 'flex-end',
        justifyContent: 'center',
        marginBottom: SPACING.xs,
    },
    currency: {
        color: COLORS.text,
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 8,
        marginRight: 4,
    },
    price: {
        color: COLORS.text,
        fontSize: 48,
        fontWeight: 'bold',
    },
    period: {
        color: COLORS.textSecondary,
        fontSize: 16,
        marginBottom: 8,
        marginLeft: 4,
    },
    cancelText: {
        color: COLORS.textSecondary,
        textAlign: 'center',
        fontSize: 14,
        marginBottom: SPACING.l,
    },
    divider: {
        height: 1,
        backgroundColor: COLORS.surfaceLight,
        marginBottom: SPACING.l,
    },
    featureRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: SPACING.m,
    },
    featureText: {
        color: COLORS.text,
        fontSize: 16,
        marginLeft: SPACING.m,
    },
    subscribeButton: {
        width: '100%',
        marginBottom: SPACING.l,
    },
    legalText: {
        color: COLORS.textSecondary,
        fontSize: 12,
        textAlign: 'center',
        lineHeight: 18,
    },
});
